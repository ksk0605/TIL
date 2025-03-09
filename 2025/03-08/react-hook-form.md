# React-Hook-Form 으로 검증 로직 리팩토링 하기

스르스르는 웹 프론트엔드 기술로 NextJS, TypeScript 를 사용하고 있다. 그리고 서비스에는 회원가입 뿐 아니라, 여러 페이지에 걸쳐 다양한 폼이 존재한다. 

다양한 페이지에 걸쳐 폼을 만들다보니 반복적인 폼 검증 코드가 늘어났고 길어지는 코드는 유지보수에 악영향을 주었다.
간단한 가입 폼에도 아래와 같이 긴 폼 검증 로직들을 반복적으로 작성해야했다. 

```js
export default function SignUpForm() {
    //... 

    const [isLoading, setIsLoading] = useState(true);
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        passwordConfirm: ""
    });
    const [errors, setErrors] = useState({
        email: "",
        password: "",
        passwordConfirm: ""
    });
    
    const { validateEmail, validatePassword } = useValidation();

    const validateForm = () => {
        const newErrors = {
            email: "",
            password: "",
            passwordConfirm: ""
        };

        if (!formData.email) {
            newErrors.email = "이메일을 입력해주세요.";
        } else if (!validateEmail(formData.email)) {
            newErrors.email = "올바른 이메일 형식이 아닙니다.";
        }

        if (!formData.password) {
            newErrors.password = "비밀번호를 입력해주세요.";
        } else if (!validatePassword(formData.password)) {
            newErrors.password = "비밀번호는 영문, 숫자를 포함하여 8자 이상이어야 합니다.";
        }

        if (formData.password !== formData.passwordConfirm) {
            newErrors.passwordConfirm = "비밀번호가 일치하지 않습니다.";
        }

        // ... 

        setErrors(newErrors);
        return !Object.values(newErrors).some(error => error !== "");
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setErrors(prev => ({
            ...prev,
            [name]: ""
        }));
    };

    const handleAgreementChange = (newAgreements: Agreement[]) => {
        setAgreements(newAgreements);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (validateForm()) {
            try {
                const response = await sendEmailCode(formData.email, true);
                updateSignUpForm({
                    email: formData.email,
                password: formData.password,
                agreements: agreements,
                sessionId: response.sessionId
                });
                router.push("/auth/signup/verify-email");
            } catch (error : any) {
                alert(error.message);
            }
        }
    };

    // UI 로직
    if (isLoading) {
        return (
            <div className="flex justify-center items-center min-h-[400px]">
                <Spinner />
            </div>
        );
    }

    return (
            <div className="mx-auto mt-2">
                <form className="space-y-3" onSubmit={handleSubmit}>
                    <EmailInput
                        email={formData.email}
                        error={errors.email}
                        onChange={handleChange}
                    />

                    <PasswordInput
                        password={formData.password}
                        passwordConfirm={formData.passwordConfirm}
                        errors={{
                            password: errors.password,
                            passwordConfirm: errors.passwordConfirm
                        }}
                        onChange={handleChange}
                    />

                    {termsError && (
                        <p className="text-red-500 text-sm">{termsError}</p>
                    )}

                    {terms && (
                        <TermsAgreement
                            terms={terms.terms}
                            onChange={handleTermsChange}
                            onAgreementChange={handleAgreementChange}
                        />
                    )}

                    <Button
                        type="submit"
                        className="w-full h-12"
                        onClick={handleSubmit}
                    >
                        다음으로
                    </Button>
                </form>
            </div>
    );
}

// 폼 검증 커스텀 훅 
export const useValidation = () => {
    const validateEmail = (email: string): boolean => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validatePassword = (password: string): boolean => {
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
        return passwordRegex.test(password);
    };

    return {
        validateEmail,
        validatePassword
    };
};
```

이는 장기적으로 여러 문제가 존재할 수 있지만 우리팀에게 가장 큰 문제는 생산성이었다. 
빠른 출시를 목표로 개발일정을 조율하고 있던 팀에게 빠른 생산성을 중요한 문제였기 때문에 
반복적인 폼 검증로직 개발을 효율적으로 할 수 있는 방법이 필요했다.

그리고 폼 개발을 위한 신뢰성 있는 기술을 찾다가 React-hook-form 을 알게 되었다.

## react-hook-form 의 장점

1. 성능 최적화
- 불필요한 리렌더링 최소화
- 제어 컴포넌트(Controlled Components) 대신 비제어 컴포넌트 사용
- 렌더링 최적화를 위한 별도 작업 불필요

2. 사용 편의성
- useForm 훅 만으로 간단하게 폼 관련 로직 구현 가능
```typescript
// 간단한 사용 예시
const { register, handleSubmit } = useForm();
const onSubmit = (data) => console.log(data);

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register("name")} />
  <button type="submit">제출</button>
</form>
```

3. 강력한 유효성 검사
```typescript
const { register } = useForm({
  defaultValues: {
    name: "",
    email: ""
  },
  mode: "onChange"
});

<input {...register("email", {
  required: "이메일은 필수입니다",
  pattern: {
    value: /\S+@\S+\.\S+/,
    message: "이메일 형식이 올바르지 않습니다"
  }
})} />
```

4. TypeScript 지원
```typescript
interface IFormInputs {
  name: string;
  email: string;
}

const { register } = useForm<IFormInputs>();
```

5. 다양한 상태 관리
- error, 더티(dirty) 체크 등 여러 상태 관리 지원
```typescript
const {
  formState: { errors, isDirty, isSubmitting, touchedFields, submitCount }
} = useForm();
```
6. 폼 상태 추적
- 더티(dirty) 체크
- 터치(touched) 필드 추적
- 제출 상태 관리

7. 디버깅 용이성
```typescript
const { watch } = useForm();
console.log(watch()); // 실시간으로 모든 필드 값 확인
```

8. 에러 핸들링
```typescript
const {
  formState: { errors },
  setError
} = useForm();

// 커스텀 에러 설정
setError("name", {
  type: "manual",
  message: "이름이 중복되었습니다"
});
```

## 코드 리팩토링 결과

react-hook-form 의 도입으로 폼 코드는 아래와 같이 리팩토링되었다.

```js
interface SignUpFormData {
    email: string;
    password: string;
    passwordConfirm: string;
}

export default function SignUpForm() {
    const { updateSignUpForm } = useSignUpFormContext();
    const [isLoading, setIsLoading] = useState(true);
    const { validateEmail, validatePassword } = useValidation();

    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
        setError,
        clearErrors
    } = useForm<SignUpFormData>({
        mode: "onChange",
        defaultValues: {
            email: "",
            password: "",
            passwordConfirm: ""
        }
    });

    const password = watch("password");

    const onSubmit = async (data: SignUpFormData) => {
        if (!isTermsValid) {
            setTermsError("필수 약관에 모두 동의해주세요.");
            return;
        }

        try {
            const response = await sendEmailCode(data.email, true);
            updateSignUpForm({
                email: data.email,
                password: data.password,
                agreements: agreements,
                sessionId: response.sessionId
            });
            router.push("/auth/signup/verify-email");
        } catch (error: any) {
            alert(error.message);
        }
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center min-h-[400px]">
                <Spinner />
            </div>
        );
    }

    return (
        <div className="mx-auto mt-2">
            <form className="space-y-3" onSubmit={handleSubmit(onSubmit)}>
                <h2 className="text-lg font-medium mb-2">이메일 입력</h2>
                <EmailInput
                    {...register("email", {
                        required: "이메일을 입력해주세요.",
                        validate: (value) =>
                            validateEmail(value) || "올바른 이메일 형식이 아닙니다."
                    })}
                    error={errors.email?.message}
                />

                <h2 className="text-lg font-medium mb-2">비밀번호 입력</h2>
                <PasswordInput
                    {...register("password", {
                        required: "비밀번호를 입력해주세요.",
                        validate: (value) =>
                            validatePassword(value) ||
                            "비밀번호는 영문, 숫자를 포함하여 8자 이상이어야 합니다."
                    })}
                    confirmProps={register("passwordConfirm", {
                        required: "비밀번호 확인을 입력해주세요.",
                        validate: (value) =>
                            value === password || "비밀번호가 일치하지 않습니다."
                    })}
                    errors={{
                        password: errors.password?.message,
                        passwordConfirm: errors.passwordConfirm?.message
                    }}
                />

                <h2 className="text-lg font-medium mb-2">약관 동의</h2>

                {termsError && (
                    <p className="text-red-500 text-sm">{termsError}</p>
                )}

                {terms && (
                    <TermsAgreement
                        terms={terms.terms}
                        onChange={handleTermsChange}
                        onAgreementChange={handleAgreementChange}
                    />
                )}

                <Button
                    type="submit"
                    className="w-full h-12"
                >
                    다음으로
                </Button>
            </form>
            <div className="mt-16"></div>
        </div>
    );
}
```

불필요한 공통 유틸을 효과적으로 제거하고 흩어져있는 여러 검증 로직들을 줄임으로 더 높은 가독성과 유지보수성, 생산성을 얻을 수 있었다. 

구체적인 개선사항은 다음과 같다:

1. 코드 응집도 향상
   - 폼 관련 로직이 한 곳에 모여 있음
   - validation 규칙이 각 필드 옆에 명확하게 정의됨
   - 타입 안정성이 향상됨 (SignUpFormData 인터페이스 활용)

2. 상태 관리 단순화
   - useState로 관리하던 여러 상태값들이 제거됨
   - errors, watch 등 내장 기능으로 상태 관리가 간편해짐
   - 불필요한 리렌더링이 감소

3. 유효성 검증 개선
   - 즉각적인 유효성 검증 (mode: "onChange")
   - 비밀번호 확인 등 연관 필드 검증이 용이
   - 에러 메시지 처리가 일관적이고 깔끔해짐

4. 개발 생산성 향상
   - 반복적인 이벤트 핸들러 코드 제거
   - register 함수로 인한 보일러플레이트 감소
   - 폼 상태 디버깅이 용이

5. 사용자 경험 개선
   - 실시간 유효성 검증으로 즉각적인 피드백
   - 일관된 에러 메시지 표시
   - 폼 제출 과정의 안정성 향상

이러한 개선사항들로 인해 폼 관련 코드의 품질이 전반적으로 향상되었으며, 향후 유지보수와 기능 확장이 더욱 용이해졌다.

## Reference 
* [react-hook-form을 선택한 이유와 적용 과정](https://tech.inflab.com/202207-rallit-form-refactoring/react-hook-form/)