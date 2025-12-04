import customtkinter as ctk
import tkinter as tk

# Thiết lập giao diện
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue") 

# Hằng số màu sắc và kích thước
MAIN_BG_COLOR = "#2B2D30"   
SECONDARY_BG_COLOR = "#3A3D42"  
ACCENT_COLOR = "#3498DB" 
FORM_WIDTH = 900
FORM_HEIGHT = 600

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ Thống Quản Lý Tài Khoản (LDPlayer 9 Control)")
        self.configure(fg_color=MAIN_BG_COLOR)
        
        # Căn giữa màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (FORM_WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (FORM_HEIGHT / 2))
        self.geometry(f"{FORM_WIDTH}x{FORM_HEIGHT}+{x_coordinate}+{y_coordinate}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_content_area()
        self.show_account_management() 

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=MAIN_BG_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # Tiêu đề Menu
        ctk.CTkLabel(self.sidebar_frame, text="🛠️ MENU HỆ THỐNG", 
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT_COLOR).grid(row=0, column=0, padx=20, pady=(20, 10))

        # Danh sách nút Sidebar (Text, Command, Row)
        menu_items = [
            ("--- QUẢN LÝ ---", None, 1),
            ("👤 Quản Lý Acc", self.show_account_management, 2),
            ("⚙️ Cấu Hình Chung", self.show_general_settings, 3),
            ("--- CÔNG CỤ HỆ THỐNG ---", None, 4),
            ("💻 Phần Mềm & Công Cụ", self.show_software_management, 5),
            ("🔗 Kết Nối LD9 & Android", self.show_ld9_connection_management, 6),
        ]

        for text, command, row in menu_items:
            if text.startswith("---"):
                ctk.CTkLabel(self.sidebar_frame, text=text, anchor="w", text_color="#999999").grid(row=row, column=0, padx=20, pady=(20 if row > 1 else 5, 5), sticky="w")
            else:
                ctk.CTkButton(self.sidebar_frame, text=text, command=command,
                              fg_color="transparent", hover_color=SECONDARY_BG_COLOR,
                              anchor="w", font=ctk.CTkFont(size=14)).grid(row=row, column=0, padx=20, pady=5, sticky="ew")

    def create_main_content_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=SECONDARY_BG_COLOR)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_status(self, message):
        if hasattr(self, 'status_label'):
             self.status_label.configure(text=f"[STATUS] {message}")
             
    # --- CÁC HÀM HELPER ĐỂ RÚT GỌN CODE ---

    def _create_task_section(self, parent, tasks, start_row, title, title_color="#F39C12"):
        """Hàm helper tạo khu vực Tác vụ Tự động Hóa."""
        ctk.CTkLabel(parent, text=title, 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color=title_color).grid(row=start_row, column=0, padx=10, pady=(10, 5), sticky="w")
        
        tasks_frame = ctk.CTkFrame(parent, fg_color=MAIN_BG_COLOR)
        tasks_frame.grid(row=start_row + 1, column=0, padx=10, pady=(0, 20), sticky="ew")
        tasks_frame.grid_columnconfigure((0, 1), weight=1)
        
        for i, (text, status_msg) in enumerate(tasks):
            ctk.CTkCheckBox(tasks_frame, text=text).grid(row=i, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkButton(tasks_frame, text="Chạy Task", width=100, 
                          command=lambda m=status_msg: self.update_status(m)).grid(row=i, column=1, padx=15, pady=5, sticky="e")
        return start_row + 2
    
    def _create_setting_group(self, content_container, title, settings, start_row):
        """Hàm helper tạo nhóm setting trong màn hình Cấu hình Chung."""
        row_count = start_row
        ctk.CTkLabel(content_container, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="#F39C12").grid(row=row_count, column=0, columnspan=2, pady=(15, 5), sticky="w")
        row_count += 1
        for label_text, placeholder, is_checkbox in settings:
            if is_checkbox:
                ctk.CTkCheckBox(content_container, text=label_text).grid(row=row_count, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            elif label_text:
                ctk.CTkLabel(content_container, text=label_text, anchor="w").grid(row=row_count, column=0, padx=10, pady=5, sticky="w")
                if placeholder:
                    ctk.CTkEntry(content_container, placeholder_text=placeholder).grid(row=row_count, column=1, padx=10, pady=5, sticky="ew")
                else: # Dành cho trường hợp đặc biệt như Auth Proxy
                    proxy_auth_frame = ctk.CTkFrame(content_container, fg_color="transparent")
                    proxy_auth_frame.grid(row=row_count, column=1, padx=10, pady=5, sticky="ew")
                    proxy_auth_frame.grid_columnconfigure((0, 1), weight=1)
                    ctk.CTkEntry(proxy_auth_frame, placeholder_text="Username").grid(row=0, column=0, sticky="ew", padx=(0, 5))
                    ctk.CTkEntry(proxy_auth_frame, placeholder_text="Password", show="*").grid(row=0, column=1, sticky="ew", padx=(5, 0))
            row_count += 1
        return row_count

    # --- CÁC PHƯƠNG THỨC MÀN HÌNH CHÍNH ---

    def show_account_management(self):
        self.clear_main_frame()
        content_container = ctk.CTkFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR)
        content_container.grid(row=0, column=0, sticky="n", padx=20, pady=20)
        content_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content_container, text="QUẢN LÝ TÀI KHOẢN MẠNG XÃ HỘI", 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color=ACCENT_COLOR).grid(row=0, column=0, pady=(10, 30))

        button_container = ctk.CTkFrame(content_container, fg_color=SECONDARY_BG_COLOR)
        button_container.grid(row=1, column=0, pady=20, sticky="n")
        
        accounts = [
            ("🎵 Acc TikTok", "lightgreen", "#33FF33", self.show_tiktok_management),
            ("📘 Acc Facebook", "#3B5998", "#FFFFFF", self.show_facebook_management),
            ("📸 Acc Instagram", "#C13584", "#FFFFFF", self.show_instagram_management),
        ]

        for i, (text, color, text_color, command_func) in enumerate(accounts):
            ctk.CTkButton(button_container, text=text, text_color=text_color,
                          font=ctk.CTkFont(size=16, weight="bold"),
                          fg_color=color, hover_color=color, width=180, height=50,
                          command=command_func).grid(row=0, column=i, padx=15)
            
        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Vui lòng chọn tài khoản để tiếp tục.", 
                                         text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")

    def show_tiktok_management(self):
        self.clear_main_frame()
        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="TÀI KHOẢN TIKTOK & TỰ ĐỘNG HÓA")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content_container, text="🎵 QUẢN LÝ TIKTOK", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#33FF33").grid(row=0, column=0, pady=(10, 20), sticky="w")

        input_export_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        input_export_frame.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="ew")
        input_export_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(input_export_frame, text="📥 Tải Lên Danh Sách Tài Khoản", fg_color=ACCENT_COLOR, hover_color="#2A73B5", command=lambda: self.update_status("Đã nhấn Tải Lên...")).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(input_export_frame, text="📤 Xuất Dữ Liệu Tài Khoản", fg_color="#F39C12", hover_color="#D68910", command=lambda: self.update_status("Đã nhấn Xuất Dữ Liệu...")).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(content_container, text="📊 Danh Sách Tài Khoản (Đã Tải Lên)", font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT_COLOR).grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")
        table_placeholder = ctk.CTkTextbox(content_container, height=150, fg_color=SECONDARY_BG_COLOR, text_color="#AAAAAA")
        table_placeholder.insert("0.0", "Username | Tình trạng | Số Followers | Proxy\n-------------------------------------------------\nExample_1 | Hoạt động | 1.2K | 192.168.1.1:8888\n...")
        table_placeholder.configure(state="disabled")
        table_placeholder.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ew")

        tasks = [
            ("Tự động Follow theo danh sách UID", "Đang chạy Tự động Follow..."),
            ("Tự động Thích Video theo Hashtag/Link", "Đang chạy Tự động Thích Video..."),
            ("Tự động Comment ngẫu nhiên", "Đang chạy Tự động Comment...")
        ]
        self._create_task_section(content_container, tasks, 4, "🤖 Tác Vụ Tự Động Hóa")
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Quản lý tài khoản TikTok.", text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")
        
    def show_facebook_management(self):
        self.clear_main_frame()
        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="TÀI KHOẢN FACEBOOK & TỰ ĐỘNG HÓA")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content_container, text="📘 QUẢN LÝ FACEBOOK", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B5998").grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        row_count = 1
        
        ctk.CTkLabel(content_container, text="📝 Quản Lý Nội Dung & Trang", font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT_COLOR).grid(row=row_count, column=0, padx=10, pady=(10, 5), sticky="w")
        content_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        content_frame.grid(row=row_count + 1, column=0, padx=10, pady=(0, 20), sticky="ew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(content_frame, text="📅 Lên Lịch Bài Đăng Mới", fg_color="#27AE60", hover_color="#1E8449", command=lambda: self.update_status("Đã nhấn Lên Lịch Bài Đăng FB")).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(content_frame, text="📜 Quản Lý Danh Sách Pages/Groups", fg_color="#F39C12", hover_color="#D68910", command=lambda: self.update_status("Đã nhấn Quản Lý Pages FB")).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        row_count += 2
        
        tasks_fb = [
            ("Tự động Phản ứng (Reaction) bài viết", "Đang chạy Tự động Reaction FB..."),
            ("Tự động Comment theo mẫu", "Đang chạy Tự động Comment FB...")
        ]
        row_count = self._create_task_section(content_container, tasks_fb, row_count, "💬 Tác Vụ Tương Tác")

        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Quản lý tài khoản Facebook.", text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")
        
    def show_instagram_management(self):
        self.clear_main_frame()
        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="TÀI KHOẢN INSTAGRAM & TỰ ĐỘNG HÓA")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content_container, text="📸 QUẢN LÝ INSTAGRAM", font=ctk.CTkFont(size=24, weight="bold"), text_color="#C13584").grid(row=0, column=0, pady=(10, 20), sticky="w")

        row_count = 1
        
        ctk.CTkLabel(content_container, text="🖼️ Quản Lý Media & Hashtag", font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT_COLOR).grid(row=row_count, column=0, padx=10, pady=(10, 5), sticky="w")
        media_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        media_frame.grid(row=row_count + 1, column=0, padx=10, pady=(0, 20), sticky="ew")
        media_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(media_frame, text="📤 Tải Lên/Đăng Ảnh Hàng Loạt", fg_color="#27AE60", hover_color="#1E8449", command=lambda: self.update_status("Đã nhấn Đăng Ảnh Hàng Loạt IG")).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkEntry(media_frame, placeholder_text="Hashtag mặc định...").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        row_count += 2
        
        followers_tasks = [
            ("Tự động Follow theo danh sách đối thủ", "Đang chạy Tự động Follow IG..."),
            ("Tự động Unfollow người không theo dõi lại", "Đang chạy Tự động Unfollow IG...")
        ]
        row_count = self._create_task_section(content_container, followers_tasks, row_count, "👥 Tác Vụ Followers")

        interaction_tasks = [
            ("Tự động Thích/Lưu bài viết theo Hashtag", "Đang chạy Tự động Thích/Lưu IG...")
        ]
        row_count = self._create_task_section(content_container, interaction_tasks, row_count, "✨ Tác Vụ Tương Tác Khác")

        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Quản lý tài khoản Instagram.", text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")


    def show_software_management(self):
        self.clear_main_frame()
        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="TÌNH TRẠNG PHẦN MỀM HỖ TRỢ")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(content_container, text="💻 QUẢN LÝ PHẦN MỀM & CÔNG CỤ HỆ THỐNG", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#E74C3C").grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")

        row_count = 1
        
        software_list = [
            ("🌐 Chrome Driver", "Phiên bản: 125.0.6422", "Cập nhật", "#2ECC71"),
            ("🦊 Firefox GeckoDriver", "Phiên bản: 0.34.0", "Cài đặt", "#3498DB"),
            ("🔒 VPN Client", "Trạng thái: Đã kết nối", "Ngắt kết nối", "#F39C12"),
            ("📦 Thư viện Requests", "Phiên bản: 2.31.0", "Kiểm tra", "#9B59B6"),
        ]

        for name, version, action_text, color in software_list:
            software_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
            software_frame.grid(row=row_count, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            software_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(software_frame, text=name, font=ctk.CTkFont(size=16, weight="bold"), text_color=color).grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")
            ctk.CTkLabel(software_frame, text=version, text_color="#AAAAAA").grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")
            
            ctk.CTkButton(software_frame, text=action_text, fg_color=color, hover_color=color, width=120, 
                          command=lambda n=name, a=action_text: self.update_status(f"Đã thực hiện: {a} {n}")
                          ).grid(row=0, column=1, rowspan=2, padx=15, pady=10, sticky="e")
            
            row_count += 1
            
        ctk.CTkLabel(content_container, text="➕ Thêm Công Cụ Mới (Tùy chỉnh)", font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT_COLOR).grid(row=row_count, column=0, columnspan=2, pady=(20, 5), sticky="w")
        new_tool_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        new_tool_frame.grid(row=row_count + 1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        new_tool_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkEntry(new_tool_frame, placeholder_text="Tên Công Cụ...").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(new_tool_frame, text="🔍 Kiểm Tra/Cài Đặt", fg_color="#E67E22", hover_color="#D35400", 
                      command=lambda: self.update_status("Đang tìm kiếm/cài đặt công cụ tùy chỉnh...")
                      ).grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Quản lý phần mềm hỗ trợ hệ thống.", text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")


    def show_ld9_connection_management(self):
        """Hiển thị giao diện Quản lý Kết nối LDPlayer 9 (Android Multi-Control)."""
        self.clear_main_frame()

        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="TRẠNG THÁI KẾT NỐI THIẾT BỊ ANDROID")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(0, weight=1)

        # Tiêu đề
        ctk.CTkLabel(content_container, text="🔗 KẾT NỐI & ĐIỀU KHIỂN LDPlayer 9 (ADB)", 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color="#FF4500").grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        row_count = 1

        # --- Khu vực 1: Tác vụ Kết nối nhanh ---
        ctk.CTkLabel(content_container, text="🚀 Tác Vụ Kết Nối Nhanh", 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color=ACCENT_COLOR).grid(row=row_count, column=0, padx=10, pady=(10, 5), sticky="w")
        row_count += 1
        
        connect_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        connect_frame.grid(row=row_count, column=0, padx=10, pady=(0, 20), sticky="ew")
        connect_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(connect_frame, text="🔍 Tự Động Kết Nối Lại ADB", fg_color="#27AE60", hover_color="#1E8449", 
                      command=lambda: self.update_status("Đang quét và kết nối lại các phiên bản LDPlayer 9...")).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(connect_frame, text="🔌 Tắt Toàn Bộ Giả Lập & Ngắt Kết Nối", fg_color="#E74C3C", hover_color="#C0392B", 
                      command=lambda: self.update_status("Đã gửi lệnh tắt tất cả các phiên bản LDPlayer 9.")).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        row_count += 1
        
        # --- Khu vực 2: Danh sách Thiết bị Đang kết nối (Placeholder) ---
        ctk.CTkLabel(content_container, text="📊 Danh Sách Thiết Bị LDPlayer (Đã Kết Nối)", 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color=ACCENT_COLOR).grid(row=row_count, column=0, padx=10, pady=(10, 5), sticky="w")
        row_count += 1
        
        table_placeholder = ctk.CTkTextbox(content_container, height=150, fg_color=SECONDARY_BG_COLOR, text_color="#AAAAAA")
        table_placeholder.insert("0.0", "Device ID | Android Ver | Cổng ADB | Tình trạng\n-------------------------------------------------\nEmulator_0 | 7.1.2 | 5555 | Đã kết nối (Sẵn sàng)\nEmulator_1 | 9.0 | 5557 | Bận (Đang chạy Task)\nEmulator_2 | 9.0 | N/A | Offline (Chưa chạy)\n...")
        table_placeholder.configure(state="disabled")
        table_placeholder.grid(row=row_count, column=0, padx=10, pady=(0, 20), sticky="ew")
        row_count += 1
        
        # --- Khu vực 3: Tùy chỉnh Cấu hình LDPlayer Engine ---
        ctk.CTkLabel(content_container, text="⚙️ Cấu Hình LDPlayer 9 Engine", 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color="#F39C12").grid(row=row_count, column=0, padx=10, pady=(10, 5), sticky="w")
        row_count += 1
        
        config_frame = ctk.CTkFrame(content_container, fg_color=MAIN_BG_COLOR)
        config_frame.grid(row=row_count, column=0, padx=10, pady=(0, 20), sticky="ew")
        config_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(config_frame, text="Đường dẫn thư mục LDPlayer:", anchor="w").grid(row=0, column=0, padx=15, pady=5, sticky="w")
        ctk.CTkEntry(config_frame, placeholder_text="Ví dụ: C:\\LDPlayer\\LDPlayer9").grid(row=0, column=1, padx=15, pady=5, sticky="ew")
        
        ctk.CTkCheckBox(config_frame, text="Tự động khởi động lại dịch vụ ADB khi lỗi").grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        
        ctk.CTkButton(config_frame, text="Lưu Cấu Hình & Kiểm Tra", fg_color=ACCENT_COLOR, hover_color="#2A73B5", 
                      command=lambda: self.update_status("Đã lưu cấu hình và kiểm tra kết nối ADB với LDPlayer.")).grid(row=2, column=1, padx=15, pady=10, sticky="e")
        row_count += 1

        self.status_label = ctk.CTkLabel(self.main_frame, text="Sẵn sàng. Quản lý kết nối LDPlayer 9 và thiết bị Android.", 
                                         text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")


    def show_general_settings(self):
        self.clear_main_frame()
        content_container = ctk.CTkScrollableFrame(self.main_frame, fg_color=SECONDARY_BG_COLOR, label_text="⭐ CẤU HÌNH HỆ THỐNG CHUNG ⭐")
        content_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_container.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(content_container, text="Thiết Lập Mặc Định Cho Tất Cả Các Tool", 
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT_COLOR).grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")
        
        row_count = 1
        
        # Cấu hình Proxy
        row_count = self._create_setting_group(content_container, "🌐 Cấu Hình Proxy (Toàn cục)", [
            ("Địa chỉ Proxy (IP:Port):", "Ví dụ: 192.168.1.1:8888", False),
            ("Tài khoản/Mật khẩu (Tùy chọn):", None, False),
        ], row_count)

        # Thiết lập Độ trễ
        row_count = self._create_setting_group(content_container, "⏳ Thiết Lập Độ Trễ & Giới Hạn", [
            ("Thời gian chờ tối thiểu (giây):", "3 (Giây)", False),
            ("Thời gian chờ tối đa (giây):", "10 (Giây)", False),
            ("Giới hạn tác vụ hàng ngày:", "500 (Ví dụ: 500 lượt follow)", False),
        ], row_count)

        # Tùy chọn Hệ thống
        row_count = self._create_setting_group(content_container, "⚙️ Tùy Chọn Hệ Thống", [
            ("Bật chế độ ghi Log chi tiết vào file (.txt)", None, True),
            ("Tự động kiểm tra và cập nhật phiên bản mới", None, True),
        ], row_count)

        save_button = ctk.CTkButton(content_container, text="💾 Lưu Cấu Hình", 
                                     fg_color="#27AE60", hover_color="#1E8449",
                                     command=lambda: self.update_status("Đã lưu cấu hình chung thành công!"))
        save_button.grid(row=row_count, column=1, padx=10, pady=30, sticky="e")
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="Thay đổi các thiết lập mặc định và nhấn Lưu.", 
                                         text_color="#AAAAAA")
        self.status_label.grid(row=1, column=0, pady=(0, 20), sticky="s")


if __name__ == "__main__":
    app = App()
    app.mainloop()