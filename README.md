## 🔔 开始之前 Before You Begin
## 如果你只是想使用这个模组管理器，而不是进行二次开发，请直接在Release中下载相应的.exe文件即可
## If you just want to use this mod manager rather than develop it further, simply download the corresponding .exe file from the Releases section.

# 剑星模组管理器

这是一个为 PC 版《Stellar Blade》（剑星）设计的简单易用的 Mod (模组) 管理器。通过直观的图形用户界面（GUI），玩家可以轻松地安装、切换和管理他们的游戏 Mod，无需再手动复制和粘贴文件。

---

## ✨ 功能特性

* **自动扫描**: 自动检测并列出 `Mods_Folder` 文件夹中所有可用的 Mod。
* **一键应用**: 只需双击或点击按钮，即可快速应用选中的 Mod。
* **安全管理**: Mod 安装在独立的 `~Mods` 文件夹中，不修改或删除任何原始游戏文件，确保游戏本体的完整性和安全性。
* **自定义路径**: 允许用户自由设置《Stellar Blade》的游戏内容路径 (`.../SB/Content`)。
* **路径记忆**: 自动保存上次设置的游戏路径，方便下次启动时使用。
* **清晰的 UI**: 界面简洁明了，可以清晰地看到可用的 Mod 列表、每个 Mod 包含的文件数量以及当前的状态。
* **智能文件夹创建**: 首次运行时，如果必要的文件夹（如 `Mods_Folder`）不存在，程序会自动创建。
* **跨平台兼容**: 基于 Python 和 Tkinter 构建，理论上可以在 Windows, macOS 和 Linux 上运行（只要游戏本身兼容）。

---

## 🚀 如何使用

### **1. 准备工作**

* 下载此 Mod 管理器 (`.py` 或编译后的 `.exe` 文件)。
* 在你的《Stellar Blade》游戏安装目录中，找到 `.../StellarBladeDemo/SB/Content/` 路径。
* 程序会自动在该路径下创建一个名为 `Mods_Folder` 的文件夹。
* 将你下载的 Mod **以文件夹的形式** 放入 `Mods_Folder` 中。

    **正确的目录结构示例:**
    ```
    D:\Steam\steamapps\common\StellarBladeDemo\SB\Content
    │
    ├── Paks/                 <-- 游戏原始 .pak 文件所在处
    └── Mods_Folder/          <-- 将你的 Mod 文件夹放在这里
        │
        ├── Mod_A/
        │   └── xxx.pak
        │
        └── Mod_B/
            └── yyy.pak
            └── zzz.pak
    ```

### **2. 运行管理器**

1.  **启动程序**: 打开 Mod 管理器。
2.  **设置路径**: 程序会尝试自动定位路径。如果路径不正确，请手动输入你的游戏 `.../SB/Content` 目录的完整路径，然后点击 **[更新路径]** 按钮。
3.  **刷新列表**: 点击 **[刷新列表]** 按钮，管理器会扫描并显示所有在 `Mods_Folder` 中的可用 Mod。
4.  **应用 Mod**:
    * 从列表中**单击**选中你想要应用的 Mod。
    * 点击蓝色的 **[应用选中的Mod]** 大按钮。
    * 或者，直接**双击**列表中的 Mod 名称。
5.  **开始游戏**: Mod 已成功应用！现在你可以启动《Stellar Blade》享受新的外观了。

---

## 🔧 技术实现

本项目使用 **Python** 作为开发语言，并利用其内置的 **Tkinter** 库来构建图形用户界面。

### 核心类: `ModManager`

这个类是 Mod 管理的后端逻辑核心。

* **路径管理**: 负责处理游戏内容 (`Content`)、Mod 源 (`Mods_Folder`) 和 Mod 应用目标 (`Paks/~Mods`) 的所有路径。
* **配置持久化**: 通过 `mod_manager_config.json` 文件来保存用户的游戏路径设置，避免每次启动都需重新配置。
* **Mod 扫描 (`get_available_mods`)**: 遍历 `Mods_Folder`，识别包含有效文件的子文件夹作为可用的 Mod，并统计每个 Mod 的文件数。
* **Mod 应用 (`apply_mod`)**:
    1.  首先，调用 `clear_active_mod_folder` 方法，彻底清空 `Paks/~Mods` 文件夹，以移除之前安装的 Mod。
    2.  然后，将用户选中的 Mod 文件夹内的所有文件和子文件夹结构，完整地复制到 `Paks/~Mods` 文件夹中。
    3.  使用 `shutil` 库进行高效和安全的文件操作。

### 界面类: `ModManagerGUI`

这个类负责构建和管理所有用户能看到的界面元素。

* **界面布局**: 使用 `tkinter.Frame` 对窗口进行模块化分区（如路径区、信息区、列表区、按钮区）。
* **样式定制**: 通过 `ttk.Style` 提供了现代化的深色主题外观，提升了视觉体验。
* **事件驱动**: 将按钮点击 (`command`) 和列表双击 (`<Double-Button-1>`) 等用户操作，与 `ModManager` 类中的相应功能（如 `apply_mod`, `refresh_mod_list`）进行绑定。
* **状态反馈**: 通过界面底部的状态栏 (`status_label`) 和信息框 (`info_label`) 为用户提供实时的操作反馈，如 "正在应用 Mod..."、"Mod 列表已更新" 等。

---

## 🤝 如何贡献

欢迎对这个项目做出贡献！你可以通过以下方式参与进来：

1.  **报告 Bug**: 如果你发现了任何问题，请在 GitHub Issues 中提交详细的报告。
2.  **提出建议**: 对新功能或改进有任何想法？也请通过 Issues 告诉我们。
3.  **提交代码**:
    * Fork 这个仓库。
    * 创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
    * 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
    * 将分支推送到你的 Fork (`git push origin feature/AmazingFeature`)。
    * 开启一个 Pull Request。

---

## 📝 开源许可

本项目采用 [MIT License] 开源。

---

# Stellar Blade Mod Manager

A simple and user-friendly Mod Manager for the PC version of *Stellar Blade*. It provides an intuitive Graphical User Interface (GUI) that allows players to easily install, switch, and manage their game mods without the hassle of manually copying and pasting files.

---

## ✨ Features

* **Automatic Scanning**: Automatically detects and lists all available mods placed within the `Mods_Folder`.
* **One-Click Apply**: Quickly apply any selected mod with a single button click or a double-click.
* **Safe Management**: Mods are installed into a separate `~Mods` folder, ensuring that no original game files are ever modified or deleted. This keeps your game installation safe and intact.
* **Custom Game Path**: Allows users to specify the custom location of their *Stellar Blade* game content path (`.../SB/Content`).
* **Path Memory**: Automatically saves the last used game path, so you don't have to set it every time you launch the manager.
* **Clean UI**: The interface is straightforward, clearly displaying the list of available mods, the number of files in each mod, and the current status.
* **Smart Folder Creation**: On first run, the manager will automatically create the necessary folders (like `Mods_Folder`) if they don't exist.
* **Cross-Platform Potential**: Built with Python and Tkinter, it can theoretically run on Windows, macOS, and Linux (provided the game itself is compatible).

---

## 🚀 How to Use

### **1. Initial Setup**

* Download this Mod Manager (`.py` or a compiled `.exe` file).
* Navigate to your *Stellar Blade* game installation directory, specifically to the `.../StellarBladeDemo/SB/Content/` path.
* The program will automatically create a folder named `Mods_Folder` inside the `Content` directory.
* Place the mods you've downloaded **inside their own individual folders** within `Mods_Folder`.

    **Correct Directory Structure Example:**
    ```
    D:\Steam\steamapps\common\StellarBladeDemo\SB\Content
    │
    ├── Paks/                 <-- Original game .pak files are here
    └── Mods_Folder/          <-- Place your mod folders here
        │
        ├── Mod_A/
        │   └── xxx.pak
        │
        └── Mod_B/
            └── yyy.pak
            └── zzz.pak
    ```

### **2. Running the Manager**

1.  **Launch the Program**: Open the Mod Manager.
2.  **Set Path**: The program will try to use the default path. If it's incorrect, paste the full path to your game's `.../SB/Content` directory into the text box and click the **[Update Path]** button.
3.  **Refresh List**: Click the **[Refresh List]** button. The manager will scan and display all available mods from your `Mods_Folder`.
4.  **Apply a Mod**:
    * **Single-click** a mod in the list to select it.
    * Click the large blue **[Apply Selected Mod]** button.
    * Alternatively, simply **double-click** the mod's name in the list.
5.  **Play the Game**: The mod is now active! You can launch *Stellar Blade* and enjoy the new look.

---

## 🔧 Technical Implementation

This project is developed in **Python** and uses its standard **Tkinter** library for the graphical user interface.

### Core Class: `ModManager`

This class handles all the backend logic for mod management.

* **Path Management**: Manages all relevant paths: the game's `Content` directory, the mod source directory (`Mods_Folder`), and the active mod destination (`Paks/~Mods`).
* **Configuration Persistence**: Uses a `mod_manager_config.json` file to save the user's game path setting, preventing the need for reconfiguration on each launch.
* **Mod Scanning (`get_available_mods`)**: Iterates through the `Mods_Folder`, identifies subdirectories containing valid files as available mods, and counts the number of files in each.
* **Mod Application (`apply_mod`)**:
    1.  First, it calls the `clear_active_mod_folder` method to completely wipe the `Paks/~Mods` directory, ensuring any previously applied mod is removed.
    2.  Next, it copies the entire file and folder structure from the user-selected mod folder into the `Paks/~Mods` directory.
    3.  It utilizes the `shutil` library for efficient and safe file operations.

### GUI Class: `ModManagerGUI`

This class is responsible for building and managing all visual elements of the application.

* **Layout**: Uses `tkinter.Frame` to organize the window into logical sections (e.g., Path Area, Info Panel, Listbox, Button Area).
* **Custom Styling**: Implements a modern dark theme using `ttk.Style` to enhance the user experience.
* **Event Handling**: Binds user actions like button clicks (`command`) and listbox double-clicks (`<Double-Button-1>`) to the corresponding functions in the `ModManager` class (e.g., `apply_mod`, `refresh_mod_list`).
* **User Feedback**: Provides real-time feedback through a status label at the bottom of the window (`status_label`) and an info panel (`info_label`), displaying messages like "Applying mod..." or "Mod list updated."

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  **Report a Bug**: If you find an issue, please submit a detailed report in the GitHub Issues section.
2.  **Suggest an Enhancement**: Have an idea for a new feature or an improvement? Feel free to open an issue to discuss it.
3.  **Submit a Pull Request**:
    * Fork the Project.
    * Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
    * Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
    * Push to the Branch (`git push origin feature/AmazingFeature`).
    * Open a Pull Request.

---

## 📝 License

Distributed under the [MIT License].
