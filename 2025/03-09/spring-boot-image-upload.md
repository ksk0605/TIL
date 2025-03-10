# spring boot 서버에 이미지를 업로드할 수 있는 방법

1. Stream 업로드
```java
@PostMapping("/upload/stream")
public ResponseEntity<String> uploadStream(InputStream inputStream) {
    try {
        // 바이트 스트림으로 직접 처리
        byte[] bytes = inputStream.readAllBytes();
        
        // S3 등에 업로드
        s3Client.putObject(bucket, "image.jpg", new ByteArrayInputStream(bytes), metadata);
        
        return ResponseEntity.ok("업로드 성공");
    } catch (IOException e) {
        return ResponseEntity.status(500).body("업로드 실패");
    }
}
```
장점:
- 메모리 효율적 처리 가능
- 대용량 파일 처리에 적합
- 스트림 처리로 인한 유연성

단점:
- 구현이 복잡
- 에러 처리가 까다로움
- 파일 메타데이터 처리가 불편

2. MultipartFile 업로드
```java
@PostMapping("/upload/multipart")
public ResponseEntity<String> uploadMultipart(@RequestParam("file") MultipartFile file) {
    try {
        // 파일 정보 쉽게 접근
        String filename = file.getOriginalFilename();
        String contentType = file.getContentType();
        byte[] bytes = file.getBytes();

        // S3 등에 업로드
        s3Client.putObject(bucket, filename, new ByteArrayInputStream(bytes), metadata);
        
        return ResponseEntity.ok("업로드 성공");
    } catch (IOException e) {
        return ResponseEntity.status(500).body("업로드 실패");
    }
}
```
장점:
- 구현이 간단
- 파일 메타데이터 쉽게 접근
- Spring에서 기본 지원

단점:
- 메모리 사용량이 큼
- 대용량 파일 처리시 비효율적
- 동시 다중 업로드 처리가 까다로움

3. AWS Multipart 업로드
```java
@PostMapping("/upload/multipart-s3")
public ResponseEntity<String> uploadMultipartS3(@RequestBody InitiateMultipartUploadRequest request) {
    // 1. 업로드 초기화
    InitiateMultipartUploadResult initResult = s3Client.initiateMultipartUpload(request);
    String uploadId = initResult.getUploadId();

    // 2. 청크 단위로 분할 업로드
    List<PartETag> partETags = new ArrayList<>();
    for (int i = 1; i <= totalParts; i++) {
        UploadPartRequest uploadRequest = new UploadPartRequest()
            .withBucketName(bucket)
            .withKey(key)
            .withUploadId(uploadId)
            .withPartNumber(i)
            .withPartSize(partSize);
            
        UploadPartResult uploadResult = s3Client.uploadPart(uploadRequest);
        partETags.add(uploadResult.getPartETag());
    }

    // 3. 업로드 완료
    CompleteMultipartUploadRequest completeRequest = new CompleteMultipartUploadRequest()
        .withBucketName(bucket)
        .withKey(key)
        .withUploadId(uploadId)
        .withPartETags(partETags);
        
    s3Client.completeMultipartUpload(completeRequest);
    
    return ResponseEntity.ok("업로드 성공");
}
```
장점:
- 대용량 파일 처리에 최적화
- 청크 단위 업로드로 재시도 가능
- 네트워크 효율성 높음
- 병렬 업로드 가능

단점:
- 구현이 복잡
- AWS 의존성
- 상태 관리 필요

권장 사용 케이스:
1. Stream 업로드
   - 실시간 스트리밍 데이터 처리
   - 메모리 제약이 있는 환경
   
2. MultipartFile 업로드
   - 소형 파일 처리 (10MB 미만)
   - 빠른 개발이 필요한 경우
   - 간단한 파일 업로드 기능

3. AWS Multipart 업로드
   - 대용량 파일 처리
   - 안정적인 업로드가 필요한 경우
   - AWS S3를 사용하는 환경