import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import sys


class ModManager:
    """
    Stellar Blade Mod管理器核心类
    负责处理mod文件的扫描、复制和管理
    """

    def __init__(self):
        # 游戏路径配置
        self.game_base_path = r"D:\Steam\steamapps\common\StellarBladeDemo\SB\Content"
        self.mods_folder = os.path.join(self.game_base_path, "Mods_Folder")
        self.paks_path = os.path.join(self.game_base_path, "Paks")
        self.active_mod_path = os.path.join(self.paks_path, "~Mods")

        # 配置文件路径，用于保存用户设置
        self.config_file = "mod_manager_config.json"
        self.load_config()

    def load_config(self):
        """加载配置文件，如果存在的话"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.game_base_path = config.get('game_base_path', self.game_base_path)
                    self.update_paths()
            except:
                pass

    def save_config(self):
        """保存当前配置到文件"""
        config = {
            'game_base_path': self.game_base_path
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

    def update_paths(self):
        """更新所有相关路径"""
        self.mods_folder = os.path.join(self.game_base_path, "Mods_Folder")
        self.paks_path = os.path.join(self.game_base_path, "Paks")
        self.active_mod_path = os.path.join(self.paks_path, "~Mods")

    def create_necessary_folders(self):
        """创建必要的文件夹结构"""
        # 创建Mods_Folder如果不存在
        if not os.path.exists(self.mods_folder):
            os.makedirs(self.mods_folder)
            return True, "已创建Mods_Folder文件夹"
        return True, "文件夹结构已就绪"

    def get_available_mods(self):
        """扫描并返回所有可用的mod列表"""
        if not os.path.exists(self.mods_folder):
            return []

        mods = []
        # 遍历Mods_Folder中的所有子文件夹
        for item in os.listdir(self.mods_folder):
            # 路径连接
            item_path = os.path.join(self.mods_folder, item)
            # 检查是否为文件夹，过滤掉文件，只处理文件夹
            if os.path.isdir(item_path):
                # 检查是否包含实际的mod文件
                """
                Path(item_path)：将路径字符串转换为 Path 对象（来自 pathlib 模块）
                .rglob('*')：递归地搜索所有文件和文件夹
                glob = 通配符搜索
                rglob = recursive glob（递归搜索）
                '*' = 匹配所有文件名
                for _ in ...：遍历找到的所有项目, 这里我们只需要文件的数量, _ 是Python中的惯例，表示这个变量我们不会实际使用
                if _.is_file()：检查是否为文件（不是文件夹）
                1 for _ in ... if ...：生成器表达式，对每个文件生成数字1
                sum(...)：将所有的1加起来，得到文件总数
                """
                file_count = sum(1 for _ in Path(item_path).rglob('*') if _.is_file())
                # 过滤掉空文件夹，只保留包含实际mod文件的文件夹
                if file_count > 0:
                    mods.append({
                        'name': item, # mod的文件夹名称（如 "CoolMod"）
                        'path': item_path, # mod的完整路径（如 "C:\Games\Mods_Folder\CoolMod"）
                        'file_count': file_count # mod包含的文件数量（如 3）
                    })
        return mods

    def clear_active_mod_folder(self):
        """清空~Mods文件夹"""
        if os.path.exists(self.active_mod_path):
            # 删除文件夹及其所有内容
            shutil.rmtree(self.active_mod_path)
        # 重新创建空文件夹
        os.makedirs(self.active_mod_path)

    def apply_mod(self, mod_name):
        """
        应用选中的mod
        1. 清空~Mods文件夹
        2. 复制选中mod的所有文件到~Mods
        """
        try:
            # 首先清空现有的mod
            self.clear_active_mod_folder()

            # 找到对应的mod文件夹
            mod_path = os.path.join(self.mods_folder, mod_name)
            if not os.path.exists(mod_path):
                return False, f"找不到mod文件夹: {mod_name}"

            # 复制所有文件到~Mods文件夹
            # 遍历源文件夹中的所有内容
            for root, dirs, files in os.walk(mod_path):
                # 计算相对路径
                rel_path = os.path.relpath(root, mod_path)

                # 在目标文件夹中创建对应的目录结构
                if rel_path != '.':
                    dest_dir = os.path.join(self.active_mod_path, rel_path)
                    os.makedirs(dest_dir, exist_ok=True)

                # 复制所有文件
                for file in files:
                    src_file = os.path.join(root, file)
                    if rel_path == '.':
                        dest_file = os.path.join(self.active_mod_path, file)
                    else:
                        dest_file = os.path.join(self.active_mod_path, rel_path, file)
                    shutil.copy2(src_file, dest_file)

            return True, f"成功应用mod: {mod_name}"

        except Exception as e:
            return False, f"应用mod时出错: {str(e)}"


class ModManagerGUI:
    """
    图形用户界面类
    提供美观易用的界面来管理mod
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Stellar Blade Mod Manager")
        self.root.geometry("800x600")

        # 设置应用程序图标（如果有的话）
        # self.root.iconbitmap('icon.ico')

        # 创建ModManager实例
        self.mod_manager = ModManager()

        # 设置界面风格
        self.setup_styles()

        # 创建界面
        self.create_widgets()

        # 初始化
        self.initialize()

    def setup_styles(self):
        """设置界面样式，创建现代化外观"""
        style = ttk.Style()

        # 设置主题
        style.theme_use('clam')

        # 自定义颜色方案
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.accent_color = '#4a9eff'
        self.hover_color = '#5aaefd'

        # 配置根窗口背景
        self.root.configure(bg=self.bg_color)

        # 配置样式
        style.configure('Title.TLabel',
                        background=self.bg_color,
                        foreground=self.fg_color,
                        font=('Arial', 24, 'bold'))

        style.configure('Info.TLabel',
                        background=self.bg_color,
                        foreground=self.fg_color,
                        font=('Arial', 10))

        style.configure('ModButton.TButton',
                        font=('Arial', 12),
                        padding=(20, 10))

    def create_widgets(self):
        """创建所有界面组件"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(main_container,
                                text="Stellar Blade Mod Manager",
                                style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # 游戏路径设置区域
        path_frame = tk.Frame(main_container, bg=self.bg_color)
        path_frame.pack(fill=tk.X, pady=(0, 20))

        path_label = ttk.Label(path_frame, text="游戏路径:", style='Info.TLabel')
        path_label.pack(side=tk.LEFT, padx=(0, 10))

        self.path_var = tk.StringVar(value=self.mod_manager.game_base_path)
        path_entry = tk.Entry(path_frame,
                              textvariable=self.path_var,
                              bg='#3c3c3c',
                              fg=self.fg_color,
                              insertbackground=self.fg_color,
                              font=('Arial', 10))
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        update_path_btn = tk.Button(path_frame,
                                    text="更新路径",
                                    command=self.update_game_path,
                                    bg=self.accent_color,
                                    fg=self.fg_color,
                                    activebackground=self.hover_color,
                                    activeforeground=self.fg_color,
                                    relief=tk.FLAT,
                                    font=('Arial', 10),
                                    padx=15)
        update_path_btn.pack(side=tk.LEFT)

        # 信息显示区域
        info_frame = tk.Frame(main_container, bg='#3c3c3c', relief=tk.FLAT, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))

        self.info_label = ttk.Label(info_frame,
                                    text="正在扫描mod文件夹...",
                                    style='Info.TLabel',
                                    background='#3c3c3c')
        self.info_label.pack(padx=10, pady=10)

        # Mod列表区域
        list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True)

        list_label = ttk.Label(list_frame,
                               text="可用的Mods:",
                               style='Info.TLabel')
        list_label.pack(anchor=tk.W, pady=(0, 10))

        # 创建带滚动条的列表框
        list_container = tk.Frame(list_frame, bg=self.bg_color)
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.mod_listbox = tk.Listbox(list_container,
                                      yscrollcommand=scrollbar.set,
                                      bg='#3c3c3c',
                                      fg=self.fg_color,
                                      selectbackground=self.accent_color,
                                      selectforeground=self.fg_color,
                                      font=('Arial', 12),
                                      height=10)
        self.mod_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.mod_listbox.yview)

        # 绑定双击事件
        self.mod_listbox.bind('<Double-Button-1>', self.on_mod_double_click)

        # 按钮区域
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        apply_btn = tk.Button(button_frame,
                              text="应用选中的Mod",
                              command=self.apply_selected_mod,
                              bg=self.accent_color,
                              fg=self.fg_color,
                              activebackground=self.hover_color,
                              activeforeground=self.fg_color,
                              relief=tk.FLAT,
                              font=('Arial', 14, 'bold'),
                              padx=30,
                              pady=10)
        apply_btn.pack(side=tk.LEFT, padx=(0, 10))

        refresh_btn = tk.Button(button_frame,
                                text="刷新列表",
                                command=self.refresh_mod_list,
                                bg='#555555',
                                fg=self.fg_color,
                                activebackground='#666666',
                                activeforeground=self.fg_color,
                                relief=tk.FLAT,
                                font=('Arial', 12),
                                padx=20,
                                pady=10)
        refresh_btn.pack(side=tk.LEFT)

        # 状态栏
        self.status_label = ttk.Label(main_container,
                                      text="就绪",
                                      style='Info.TLabel')
        self.status_label.pack(side=tk.BOTTOM, anchor=tk.W, pady=(10, 0))

    def initialize(self):
        """初始化应用程序"""
        # 创建必要的文件夹
        success, message = self.mod_manager.create_necessary_folders()
        if not success:
            messagebox.showerror("错误", message)

        # 刷新mod列表
        self.refresh_mod_list()

    def refresh_mod_list(self):
        """刷新mod列表显示"""
        self.mod_listbox.delete(0, tk.END)

        mods = self.mod_manager.get_available_mods()

        if not mods:
            self.info_label.config(text="未找到任何mod。请将mod文件夹放入Mods_Folder中。")
            self.status_label.config(text="mod文件夹为空")
        else:
            self.info_label.config(text=f"找到 {len(mods)} 个可用的mod")
            for mod in mods:
                display_text = f"{mod['name']} ({mod['file_count']} 个文件)"
                self.mod_listbox.insert(tk.END, display_text)
            self.status_label.config(text="mod列表已更新")

    def apply_selected_mod(self):
        """应用用户选中的mod"""
        selection = self.mod_listbox.curselection()

        if not selection:
            messagebox.showwarning("提示", "请先选择一个mod")
            return

        # 获取选中的mod名称（去除文件数量信息）
        selected_text = self.mod_listbox.get(selection[0])
        mod_name = selected_text.split(' (')[0]

        # 确认对话框
        result = messagebox.askyesno("确认",
                                     f"确定要应用mod: {mod_name}?\n这将替换当前激活的mod。")

        if result:
            self.status_label.config(text=f"正在应用mod: {mod_name}...")
            self.root.update()

            success, message = self.mod_manager.apply_mod(mod_name)

            if success:
                messagebox.showinfo("成功", message)
                self.status_label.config(text=f"当前激活: {mod_name}")
            else:
                messagebox.showerror("错误", message)
                self.status_label.config(text="应用失败")

    def on_mod_double_click(self, event):
        """处理双击mod列表项事件"""
        self.apply_selected_mod()

    def update_game_path(self):
        """更新游戏路径"""
        new_path = self.path_var.get()
        self.mod_manager.game_base_path = new_path
        self.mod_manager.update_paths()
        self.mod_manager.save_config()

        # 重新初始化
        self.initialize()
        messagebox.showinfo("成功", "游戏路径已更新")


def main():
    """主函数，启动应用程序"""
    root = tk.Tk()
    app = ModManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()