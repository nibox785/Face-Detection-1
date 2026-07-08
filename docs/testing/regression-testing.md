# Regression Testing

Regression test nhằm bảo vệ các behavior đã tồn tại trước khi thay đổi code.

## Các lĩnh vực cần regression test

- Face detection output vẫn giữ cấu trúc box/confidence/landmarks.
- Quality assessment vẫn trả về visibility, quality_score, pose, status, rating.
- Endpoint /detect vẫn trả về hình ảnh và dữ liệu face đúng format.

## Mẫu test đề xuất

- So sánh output của một ảnh mẫu trước và sau khi chỉnh sửa logic.
- Kiểm tra các status label vẫn đúng với input cố định.
- Kiểm tra không làm thay đổi field names trong response.

## Ghi chú

Vì hiện tại chưa có test suite chính thức, regression test nên được thêm dần khi có sample output ổn định.
