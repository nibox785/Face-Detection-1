# Unit Testing

Tài liệu này xác định các hàm, lớp và module nên được kiểm thử ở mức unit trong repository Face Detection.

## Mục tiêu

- Bảo vệ các logic cốt lõi không phụ thuộc vào toàn bộ pipeline inference.
- Giảm rủi ro khi thay đổi các helper xử lý box, quality scoring, mask postprocessing hoặc wrapper mô hình.
- Tạo nền tảng cho các tầng kiểm thử cao hơn như component, integration và regression.

## Các module nên unit test

### 1. [backend/quality/face_quality.py](../../backend/quality/face_quality.py)

#### Mục đích
Kiểm tra logic đánh giá chất lượng khuôn mặt bằng các chỉ số như kích thước, visibility, occlusion và pose.

#### Các hàm nên test
- check_face_size
- check_visibility
- check_occlusion
- check_head_pose
- analyze_face_quality

#### Inputs
- box: tuple hoặc list chứa tọa độ bounding box
- binary_mask: ma trận nhị phân biểu diễn mask khuôn mặt
- landmarks: danh sách 10 giá trị tọa độ landmark
- confidence: điểm tin cậy từ detector

#### Outputs
- chuỗi trạng thái như Normal, Too Small, Large
- giá trị visibility từ 0 đến 100
- boolean occlusion
- chuỗi pose như Normal, Head Left, Head Right, Head Up, Head Down
- dictionary kết quả quality gồm visibility, quality_score, pose, status, rating

#### Mock requirements
- Không bắt bu mock cho logic thuần túy này.
- Chỉ cần tạo các bộ dữ liệu đầu vào giả lập để kiểm tra các nhánh điều kiện.

#### Dependencies
- NumPy
- Không phụ thuộc vào mô hình hoặc API

#### Failure cases
- box rỗng hoặc không hợp lệ
- mask rỗng
- landmarks thiếu dữ liệu
- box vượt quá kích thước mask
- confidence thấp hoặc box quá nhỏ

---

### 2. [backend/segmentation/postprocess.py](../../backend/segmentation/postprocess.py)

#### Mục đích
Kiểm tra logic chuyển logits sang binary mask dùng cho segmentation.

#### Hàm nên test
- logits_to_binary_mask

#### Inputs
- torch.Tensor hoặc numpy.ndarray chứa logits
- có thể ở dạng 2D, 3D hoặc 4D tùy theo nguồn đầu vào

#### Outputs
- numpy.ndarray kiểu uint8, kích thước HxW với các pixel thuộc face class được đặt giá trị 255

#### Mock requirements
- Không cần mock nếu dùng dữ liệu giả lập đơn giản.
- Nếu test ở mức wrapper thì có thể mock đầu ra logits từ mô hình.

#### Dependencies
- NumPy
- PyTorch
- cấu hình FACE_CLASSES từ [backend/segmentation/config.py](../../backend/segmentation/config.py)

#### Failure cases
- logits có shape không phù hợp
- tensor rỗng
- các class không nằm trong FACE_CLASSES
- đầu vào là numpy array với shape 4D

---

### 3. [backend/utils/box_utils.py](../../backend/utils/box_utils.py)

#### Mục đích
Kiểm tra các hàm hình học và decoding dùng cho box, landmark và NMS.

#### Các hàm nên test
- point_form
- center_size
- intersect
- jaccard
- matrix_iou
- matrix_iof
- match
- encode
- encode_landm
- decode
- decode_landm
- log_sum_exp
- nms

#### Inputs
- tensor hoặc numpy array biểu diễn boxes và priors
- các biến thể variance, labels, ground truth boxes, landmarks

#### Outputs
- tensor hoặc numpy array chuyển đổi box, IoU, matched targets, indices giữ lại sau NMS

#### Mock requirements
- Không cần mock cho hầu hết các hàm này.
- Với match và nms, có thể dùng fixture box giả lập để kiểm tra đường đi logic.

#### Dependencies
- PyTorch
- NumPy

#### Failure cases
- box rỗng
- box có tọa độ ngược hoặc không hợp lệ
- priors không khớp với số lượng expected
- zero-area boxes
- trường hợp không có box nào được giữ lại sau NMS

---

### 4. [backend/models/face_detector.py](../../backend/models/face_detector.py)

#### Mục đích
Kiểm tra wrapper của detector ONNX ở mức logic đầu vào và đầu ra, không cần chạy toàn bộ mô hình thật.

#### Lớp nên test
- RetinaFaceDetector

#### Inputs
- ảnh đầu vào dạng numpy array BGR
- threshold, nms_threshold, upscale

#### Outputs
- danh sách các face dict gồm box, confidence, landmarks

#### Mock requirements
- Cần mock đối tượng session của ONNX Runtime để trả về các tensor giả lập cho loc, conf, landms.
- Cần mock các hàm decode và NMS nếu mục tiêu là kiểm tra logic orchestration hơn là tính toán thật.

#### Dependencies
- OpenCV
- NumPy
- PyTorch
- ONNX Runtime
- PriorBox và các hàm decode từ [backend/utils/box_utils.py](../../backend/utils/box_utils.py)

#### Failure cases
- ảnh đầu vào không đúng shape
- confidence_threshold quá cao dẫn tới empty result
- upscale=True với ảnh nhỏ
- session inference trả về output sai shape
- model session thất bại hoặc không init được

---

### 5. [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)

#### Mục đích
Kiểm tra wrapper segmenter ONNX ở mức preprocessing và postprocessing đầu ra.

#### Lớp nên test
- UNetFaceSegmenter

#### Inputs
- ảnh crop khuôn mặt dạng numpy array BGR
- danh sách crops cho predict_batch

#### Outputs
- binary mask có shape khớp với input crop
- danh sách mask cho batch prediction

#### Mock requirements
- Cần mock session.run để trả về logits giả lập.
- Có thể mock hàm logits_to_binary_mask nếu mục tiêu là kiểm tra luồng wrapper.

#### Dependencies
- OpenCV
- NumPy
- ONNX Runtime
- [backend/segmentation/postprocess.py](../../backend/segmentation/postprocess.py)

#### Failure cases
- crop rỗng hoặc kích thước 0
- batch rỗng
- đầu vào có shape không chuẩn
- output logits không khớp expected shape

---

### 6. [backend/quality/logger.py](../../backend/quality/logger.py)

#### Mục đích
Kiểm tra logic lưu evidence ảnh và metadata.

#### Hàm nên test
- save_evidence

#### Inputs
- ảnh gốc, face crop, binary mask và metadata
- output_dir

#### Outputs
- dictionary chứa đường dẫn tới frame, crop, mask và metadata

#### Mock requirements
- Có thể mock cv2.imwrite và open để kiểm tra file được tạo đúng.

#### Dependencies
- OpenCV
- JSON và filesystem

#### Failure cases
- output_dir không tồn tại
- metadata thiếu trường id
- write file thất bại

---
