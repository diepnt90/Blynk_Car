
## Control Car with Pi3 via Blynk

Trên Blink sẽ gồm 1 button bật tắt Car thông qua V0, và JoyStick điểu khiển xe lên xuống trái phải và gửi xuống Pi qua v1 và v2.

V1 và V2 sẽ truyền thông số tọa độ x, y của JoyStick. Range x và y là từ 1 đến 2013 với 512 là mức giữa
> 512 là tiến, <512 là lùi, =512 là dừng lại. Tương tự với sang trái phải.

Các bước kết nối Pi với điện thoại để điều khiển.

1. Dùng màn hình và đăng nhập username: trangnguyen, mật khẩu = 1431989
2. Chuyển sang quyển root (admin): su -
 nhập password: 1431989
3. Bật 4g trên điện thoại và bật hostpot
4. Trên Pi gõ như sau để hiển thị wifi kết nối: nmcli device wifi list
5. Sau khi thấy tên wifi hotspot thì kết nối bằng lệnh : nmcli device wifi connect "Tên_WIFI" password "Mật_khẩu_WIFI"
Kết nối thành công trên điện thoại sẽ báo icon hình xanh xanh
6. Lấy Ip của Pi lúc này bằng lệnh: ifconfig
7. Vào Blynk rồi sửa phần xem camera chỉnh IP về đúng IP lấy bước 6. Định dạng video là http://IP:8080/?action=stream
8. Trên Pi vào môi trường Blynk bằng lệnh: source blynk_env/bin/activate
9. vào thư mục blynk_env: cd blynk_env
10. chạy file BlynkCar.py: python3 BlynkCar.py

File BlynkCar này là file kết nối đến Blynk nhận tín hiệu từ app trên điện thoại về v0, v1, v2 và dự vào đó để điểu khiển động cơ car thông qua driver bts7960

Muốn sửa file này bằng cách. Trước tiên cả 2 laptop và pi cùng mạng và lấy dc IP của PI theo bước 6 bên trên

1.  Mở putty trên máy tính nhập IP và đăng nhập trangnguyen và chuyển qua root như bước 1,2
2.  chạy: source blynk_env/bin/activate && cd blynk_env
1.  xóa file này đi: rm BlynkCar.py
2.  tạo mới file này: nano BlynkCar.py
3. Paste nội dung mới đã sửa
4. Ctrl+ X rồi bỏ ra nhấn Y để lưu
Lưu ý, file này ở trong thư mục blynk_env, sau cần sửa thì phải vào đúng thư mục này

Kết nối Pi với driver và moto như sau

![CleanShot 2025-05-24 at 16 25 33](https://github.com/user-attachments/assets/1c41d0d2-b13a-4dd8-9d0c-bace03c413f1)

Nếu chạy không chuẩn chỉ cần sửa file BlynkCar.py, phần logic điều khiển động cơ khi nhận tọa độ joystick x,y qua v1 và v2
