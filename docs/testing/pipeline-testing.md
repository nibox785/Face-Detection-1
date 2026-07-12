# Pipeline Testing

Tài liệu này tập trung vào việc kiểm thử toàn bộ luồng xử lý từ ảnh đầu vào đến kết quả trả về cho frontend thông qua endpoint /detect.

## Scope

Pipeline testing nên bảo vệ các bước thực hiện trong [backend/main.py](../../backend/main.py):
1. nhận file ảnh từ request
2. khởi tạo detector và chạy inference
3. chuẩn bị crops cho segmentation
4. chạy segmenter và tạo mask
5. tính quality assessment
6. tạo response gồm ảnh annotate, số lượng face và danh sách face metadata

## Các luồng cần kiểm thử

### 1. Luồng không phát hiện khuôn mặt

#### Mục đích
Đảm bảo hệ thống xử lý trường hợp không có phát hiện face mà không làm lỗi toàn bộ pipeline.

#### Nội dung cần kiểm tra
- detector trả về danh sách rỗng
- pipeline vẫn tạo response hợp lệ
- face_count bằng 0
- faces rỗng
- ảnh annotate vẫn được tạo thành công

### 2. Luồng phát hiện khuôn mặt và segmentation

#### Mục đích
Đảm bảo khi detector phát hiện face thì pipeline tiếp tục chạy segmentation, quality assessment và tạo dữ liệu trả về.

#### Nội dung cần kiểm tra
- mỗi face phát hiện được có thể tạo mask hoặc fallback mask
- response chứa đúng số lượng face
- mỗi face entry có các trường cần thiết như box, confidence, landmarks, mask_rle, quality_score, status, rating

### 3. Luồng fallback khi segmentation thất bại

#### Mục đích
Đảm bảo khi segmenter lỗi thì hệ thống vẫn trả về response thay vì crash.

#### Nội dung cần kiểm tra
- lỗi từ segmenter không làm endpoint thất bại toàn bộ
- hệ thống dùng fallback ellipse mask
- response vẫn có face_count và faces

### 4. Luồng xử lý box nhỏ hoặc không hợp lệ

#### Mục đích
Đảm bảo các box quá nhỏ hoặc không hợp lệ không làm pipeline sập.

#### Nội dung cần kiểm tra
- các box có diện tích nhỏ bị bỏ qua trong bước segmentation
- response vẫn ổn định
- không tạo output sai cho các face không hợp lệ

## Reference implementation

- [backend/main.py](../../backend/main.py)
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/quality/face_quality.py](../../backend/quality/face_quality.py)

## Liên hệ với tài liệu khác

Thông tin về kiến trúc và phạm vi kiểm thử có thể xem thêm tại:
- [docs/testing/testing-architecture.md](../../docs/testing/testing-architecture.md)
- [docs/testing/testing-scope.md](../../docs/testing/testing-scope.md)
- [docs/testing/integration-testing.md](../../docs/testing/integration-testing.md)
