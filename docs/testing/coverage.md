# Coverage Goals

Mục tiêu coverage nên được đặt theo mức độ hiện tại và khả năng phát triển của project.

## Mức độ ưu tiên

1. Coverage cho các hàm quality logic và mask utility nên được ưu tiên cao nhất.
2. Coverage cho endpoint /detect nên được tăng dần khi integration test hoàn thiện.
3. Coverage cho training scripts có thể thấp hơn vì đây là code huấn luyện và không phải luồng runtime chính.

## Khuyến nghị

- Bắt đầu với mục tiêu coverage 60% cho các module backend chính.
- Sau khi có integration test, tăng dần lên mức phù hợp với quy mô project.
- Không cần ép coverage quá cao cho các script training nếu không có test phù hợp.
