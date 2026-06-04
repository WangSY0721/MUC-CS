import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path
import shutil
import re


class ImageCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片检查工具")

        # 将窗口设置为全屏
        self.root.attributes('-fullscreen', True)

        # 绑定Esc键退出全屏
        self.root.bind('<Escape>', self.exit_fullscreen)

        # 配置变量
        self.target_folder = "22012646-王世屹"
        self.root_dir = Path.cwd()

        # 数据变量
        self.current_page = None
        self.current_image_index = 0
        self.image_files = []
        self.processed_dir = None
        self.page_image_photo = None

        # 新增变量用于跟踪行和列的当前值，默认值为1
        self.current_col = 1
        self.current_row = 1

        # 创建界面
        self.create_widgets()

        # 初始化
        self.load_page_folders()

    def exit_fullscreen(self, event=None):
        """退出全屏模式"""
        self.root.attributes('-fullscreen', False)

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 页面选择区域
        page_frame = ttk.LabelFrame(main_frame, text="选择页面", padding="5")
        page_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        page_frame.columnconfigure(1, weight=1)

        ttk.Label(page_frame, text="页面:").grid(row=0, column=0, padx=(0, 5))
        self.page_var = tk.StringVar()
        self.page_combo = ttk.Combobox(page_frame, textvariable=self.page_var, state="readonly")
        self.page_combo.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)
        self.page_combo.bind('<<ComboboxSelected>>', self.on_page_selected)

        # 图片显示区域
        # 左侧：page_x.png
        page_image_frame = ttk.LabelFrame(main_frame, text="页面预览", padding="5")
        page_image_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        page_image_frame.columnconfigure(0, weight=1)
        page_image_frame.rowconfigure(0, weight=1)

        self.page_canvas = tk.Canvas(page_image_frame, bg="white", width=600, height=800)
        self.page_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 中间：待检查图片
        left_frame = ttk.LabelFrame(main_frame, text="待检查图片", padding="5")
        left_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        self.left_canvas = tk.Canvas(left_frame, bg="white", width=300, height=400)
        self.left_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 右侧：正确图片
        right_frame = ttk.LabelFrame(main_frame, text="正确图片", padding="5")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.right_canvas = tk.Canvas(right_frame, bg="white", width=300, height=400)
        self.right_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 控制区域
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # 输入框区域
        input_frame = ttk.Frame(control_frame)
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # 正确与否
        ttk.Label(input_frame, text="正确与否:").grid(row=0, column=0, padx=(0, 5), pady=5)
        self.correct_var = tk.StringVar()
        self.correct_entry = ttk.Entry(input_frame, textvariable=self.correct_var, width=10)
        self.correct_entry.grid(row=0, column=1, padx=(0, 20), pady=5)

        # 列号
        ttk.Label(input_frame, text="列号:").grid(row=0, column=2, padx=(0, 5), pady=5)
        self.col_var = tk.StringVar(value=str(self.current_col))
        self.col_entry = ttk.Entry(input_frame, textvariable=self.col_var, width=10)
        self.col_entry.grid(row=0, column=3, padx=(0, 20), pady=5)

        # 行号
        ttk.Label(input_frame, text="行号:").grid(row=0, column=4, padx=(0, 5), pady=5)
        self.row_var = tk.StringVar(value=str(self.current_row))
        self.row_entry = ttk.Entry(input_frame, textvariable=self.row_var, width=10)
        self.row_entry.grid(row=0, column=5, padx=(0, 20), pady=5)

        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        self.confirm_btn = ttk.Button(button_frame, text="确认", command=self.confirm_action)
        self.confirm_btn.grid(row=0, column=0, padx=(0, 10))

        self.remove_btn = ttk.Button(button_frame, text="移除", command=self.remove_action)
        self.remove_btn.grid(row=0, column=1, padx=(10, 0))

        # 状态信息
        self.status_var = tk.StringVar(value="请选择页面")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # 进度信息
        self.progress_var = tk.StringVar(value="")
        progress_label = ttk.Label(control_frame, textvariable=self.progress_var, foreground="green")
        progress_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))

    def load_page_folders(self):
        """加载页面文件夹列表"""
        target_dir = self.root_dir / self.target_folder

        if not target_dir.exists():
            messagebox.showerror("错误", f"目标文件夹 {target_dir} 不存在")
            return

        # 查找所有以page_开头的文件夹
        page_folders = []
        for item in target_dir.iterdir():
            if item.is_dir() and item.name.startswith('page_'):
                page_folders.append(item.name)

        if not page_folders:
            messagebox.showwarning("警告", "未找到任何page_文件夹")
            return

        # 更新下拉框
        self.page_combo['values'] = sorted(page_folders)
        if page_folders:
            self.page_combo.set(page_folders[0])
            self.on_page_selected()

    def on_page_selected(self, event=None):
        """页面选择事件"""
        self.current_page = self.page_var.get()
        if not self.current_page:
            return

        # 加载图片文件列表
        target_dir = self.root_dir / self.target_folder
        page_dir = target_dir / self.current_page

        if not page_dir.exists():
            messagebox.showerror("错误", f"页面文件夹 {page_dir} 不存在")
            return

        # 获取PNG文件列表
        self.image_files = list(page_dir.glob("*.png"))
        self.image_files.sort()

        # 创建处理后的文件夹
        self.processed_dir = target_dir / f"processed_{self.current_page}"
        self.processed_dir.mkdir(exist_ok=True)

        # 重置索引
        self.current_image_index = 0

        # 重置行和列的计数器为默认值
        self.current_col = 1
        self.current_row = 1
        self.col_var.set(str(self.current_col))
        self.row_var.set(str(self.current_row))

        # 显示第一张图片
        if self.image_files:
            self.show_current_image()
        else:
            messagebox.showinfo("信息", f"页面 {self.current_page} 中没有找到PNG文件")

        # 加载并显示 page_x.png
        self.show_page_image()

    def show_page_image(self):
        """显示对应的 page_x.png"""
        # 从文件夹名中提取页码
        page_number_match = re.match(r'page_(\d+)', self.current_page)
        if not page_number_match:
            self.page_canvas.delete("all")
            self.page_canvas.create_text(
                self.page_canvas.winfo_width() / 2,
                self.page_canvas.winfo_height() / 2,
                text="无法解析页码",
                fill="red",
                justify="center"
            )
            return

        page_number = page_number_match.group(1)
        # 修正路径：page_x.png 位于 22012663-叶璟霖/ 文件夹内，与 page_61 等文件夹同级
        page_image_path = self.root_dir / self.target_folder / f"page_{page_number}.png"

        if page_image_path.exists():
            canvas_width = self.page_canvas.winfo_width()
            canvas_height = self.page_canvas.winfo_height()

            if canvas_width <= 1:
                # 调整默认尺寸，以适应更大的页面预览区域
                canvas_width, canvas_height = 800, 800

            try:
                img = Image.open(page_image_path)
                img_width, img_height = img.size
                scale = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                self.page_image_photo = ImageTk.PhotoImage(img)

                self.page_canvas.delete("all")
                self.page_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.page_image_photo,
                                              anchor="center")

            except Exception as e:
                self.page_canvas.delete("all")
                self.page_canvas.create_text(
                    self.page_canvas.winfo_width() / 2,
                    self.page_canvas.winfo_height() / 2,
                    text=f"图片加载失败: {e}",
                    fill="red",
                    justify="center"
                )
        else:
            self.page_canvas.delete("all")
            self.page_canvas.create_text(
                self.page_canvas.winfo_width() / 2,
                self.page_canvas.winfo_height() / 2,
                text=f"未找到对应 {page_image_path.name}",
                fill="orange",
                justify="center"
            )

    def show_current_image(self):
        """显示当前图片"""
        if not self.image_files or self.current_image_index >= len(self.image_files):
            self.status_var.set("所有图片处理完成")
            return

        current_file = self.image_files[self.current_image_index]
        self.display_image(current_file, self.left_canvas)
        self.show_correct_image(current_file)
        self.status_var.set(f"当前处理: {current_file.name}")
        self.progress_var.set(f"进度: {self.current_image_index + 1}/{len(self.image_files)}")
        self.parse_filename(current_file.name)

    def show_correct_image(self, source_file):
        """显示对应的正确图片"""
        number, letters = self.extract_info_from_filename(source_file.name)
        if number is None or letters is None:
            self.right_canvas.delete("all")
            self.right_canvas.create_text(
                self.right_canvas.winfo_width() / 2,
                self.right_canvas.winfo_height() / 2,
                text="无法解析文件名",
                fill="red",
                justify="center"
            )
            return

        target_dir = self.root_dir / self.target_folder
        generated_dir = target_dir / "generated_images" / self.current_page
        number_padded = f"{number:02d}"
        correct_image_path = generated_dir / f"{number_padded}_{letters}.png"

        if correct_image_path.exists():
            self.display_image(correct_image_path, self.right_canvas)
        else:
            self.right_canvas.delete("all")
            self.right_canvas.create_text(
                self.right_canvas.winfo_width() / 2,
                self.right_canvas.winfo_height() / 2,
                text="未找到对应图片",
                fill="orange",
                justify="center"
            )

    def display_image(self, image_path, canvas):
        """在画布上显示图片"""
        try:
            image = Image.open(image_path)
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            if canvas_width <= 1:
                # 调整默认大小以适应新布局
                canvas_width, canvas_height = 300, 400

            img_width, img_height = image.size
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            scale = min(scale_x, scale_y)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            canvas.delete("all")
            canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo, anchor="center")
            canvas.image = photo

        except Exception as e:
            canvas.delete("all")
            canvas.create_text(
                canvas.winfo_width() / 2,
                canvas.winfo_height() / 2,
                text=f"图片加载失败: {e}",
                fill="red",
                justify="center"
            )

    def extract_info_from_filename(self, filename):
        """从文件名中提取编号和字母串"""
        name_without_ext = os.path.splitext(filename)[0]

        pattern = r'^(\d+)_\d+_\d+_x_y_(.+)$'
        match = re.match(pattern, name_without_ext)

        if match:
            number = int(match.group(1))
            letters = match.group(2)
            return number, letters
        else:
            pattern2 = r'^(\d+)_\d+_\d+_\d+_(.+)$'
            match2 = re.match(pattern2, name_without_ext)
            if match2:
                number = int(match2.group(1))
                letters = match2.group(2)
                return number, letters
            else:
                return None, None

    def parse_filename(self, filename):
        """解析文件名并填充输入框"""
        name_without_ext = os.path.splitext(filename)[0]

        pattern = r'^(\d+)_(\d+)_(\d+)_x_y_(.+)$'
        match = re.match(pattern, name_without_ext)

        if match:
            self.correct_var.set(match.group(2))
            # 不再从文件名中填充行列，以保持默认值
            # self.col_var.set("")
            # self.row_var.set("")
        else:
            pattern2 = r'^(\d+)_(\d+)_(\d+)_(\d+)_(.+)$'
            match2 = re.match(pattern2, name_without_ext)
            if match2:
                self.correct_var.set(match2.group(2))
                # 不再从文件名中填充行列，以保持默认值
                # self.col_var.set(match2.group(3))
                # self.row_var.set(match2.group(4))
            else:
                self.correct_var.set("")
                # 不再从文件名中填充行列，以保持默认值
                # self.col_var.set("")
                # self.row_var.set("")

    def confirm_action(self):
        """确认按钮动作，增加列、行自动递增和默认值功能"""
        if not self.image_files or self.current_image_index >= len(self.image_files):
            return

        current_file = self.image_files[self.current_image_index]
        correct = self.correct_var.get().strip()

        # 检查 '正确与否' 是否为空
        if not correct:
            messagebox.showwarning("警告", "请填写正确与否")
            return

        # 获取用户输入的列号，如果为空，则使用当前值（默认值1）
        col_str = self.col_var.get().strip()
        if col_str:
            try:
                self.current_col = int(col_str)
            except ValueError:
                messagebox.showwarning("警告", "列号必须是数字")
                return

        # 获取用户输入的行号，如果为空，则使用当前值（默认值1）
        row_str = self.row_var.get().strip()
        if row_str:
            try:
                self.current_row = int(row_str)
            except ValueError:
                messagebox.showwarning("警告", "行号必须是数字")
                return

        number, letters = self.extract_info_from_filename(current_file.name)
        if number is None or letters is None:
            messagebox.showerror("错误", "无法解析原文件名")
            return

        page_number_match = re.match(r'page_(\d+)', self.current_page)
        if not page_number_match:
            messagebox.showerror("错误", "无法从页面文件夹名中解析页码")
            return
        page = page_number_match.group(1)

        # 构建新的文件名
        new_filename = f"{correct}_{page}_{self.current_col}_{self.current_row}_{letters}.png"
        new_file_path = self.processed_dir / new_filename
        try:
            shutil.copy2(current_file, new_file_path)
            messagebox.showinfo("成功", f"文件已保存为: {new_filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {e}")
            return

        # 确认后，行号自动加1
        self.current_row += 1
        self.row_var.set(str(self.current_row))

        self.next_image()

    def remove_action(self):
        """移除按钮动作"""
        if not self.image_files or self.current_image_index >= len(self.image_files):
            return

        # 移除后，行号自动加1
        self.current_row += 1
        self.row_var.set(str(self.current_row))
        self.next_image()

    def next_image(self):
        """移动到下一张图片"""
        self.current_image_index += 1
        if self.current_image_index < len(self.image_files):
            self.show_current_image()
        else:
            self.status_var.set("所有图片处理完成")
            self.progress_var.set(f"进度: {len(self.image_files)}/{len(self.image_files)}")
            self.left_canvas.delete("all")
            self.right_canvas.delete("all")
            self.left_canvas.create_text(250, 200, text="处理完成", fill="green", font=("Arial", 20))
            self.right_canvas.create_text(250, 200, text="处理完成", fill="green", font=("Arial", 20))

            messagebox.showinfo("完成",
                                f"页面 {self.current_page} 的所有图片处理完成！\n处理后的文件保存在: {self.processed_dir}")

    def set_target_folder(self, folder_name):
        """设置目标文件夹名称"""
        self.target_folder = folder_name
        self.load_page_folders()


def main():
    root = tk.Tk()
    app = ImageCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()