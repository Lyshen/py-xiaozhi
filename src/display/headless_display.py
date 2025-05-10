import asyncio
import logging
from typing import Optional, Callable

from src.display.base_display import BaseDisplay
from src.utils.logging_config import get_logger


class HeadlessDisplay(BaseDisplay):
    """无界面显示模式，用于服务器环境"""
    
    def __init__(self):
        super().__init__()  # 调用父类初始化
        """初始化无头显示模式"""
        self.logger = get_logger(__name__)
        self.running = True
        
        # 状态相关
        self.current_status = "未连接"
        self.current_text = "待命"
        self.current_emotion = "neutral"
        self.current_volume = 50  # 默认音量
        
        # 回调函数
        self.press_callback = None
        self.release_callback = None
        self.auto_callback = None
        self.status_callback = None
        self.text_callback = None
        self.emotion_callback = None
        self.abort_callback = None
        self.send_text_callback = None
        
        # 键盘监听器（在无头模式下不需要实际功能）
        self.keyboard_listener = None
        
    def set_callbacks(self,
                      press_callback: Optional[Callable] = None,
                      release_callback: Optional[Callable] = None,
                      status_callback: Optional[Callable] = None,
                      text_callback: Optional[Callable] = None,
                      emotion_callback: Optional[Callable] = None,
                      mode_callback: Optional[Callable] = None,
                      auto_callback: Optional[Callable] = None,
                      abort_callback: Optional[Callable] = None,
                      send_text_callback: Optional[Callable] = None):
        """设置回调函数"""
        self.press_callback = press_callback
        self.release_callback = release_callback
        self.status_callback = status_callback
        self.text_callback = text_callback
        self.emotion_callback = emotion_callback
        self.auto_callback = auto_callback
        self.abort_callback = abort_callback
        self.send_text_callback = send_text_callback
        self.logger.debug("无头模式回调函数设置完成")
    
    def start_recording(self):
        """API方法：开始录音"""
        self.logger.info("API触发：开始录音")
        if self.press_callback:
            self.press_callback()
        else:
            self.logger.error("按键回调未设置，无法开始录音")
    
    def stop_recording(self):
        """API方法：停止录音"""
        self.logger.info("API触发：停止录音")
        if self.release_callback:
            self.release_callback()
        else:
            self.logger.error("释放回调未设置，无法停止录音")
    
    def send_text(self, text):
        """API方法：发送文本"""
        self.logger.info(f"API触发：发送文本 '{text}'")
        if self.send_text_callback:
            # 获取应用程序的事件循环并在其中运行协程
            from src.application import Application
            app = Application.get_instance()
            if app and app.loop:
                asyncio.run_coroutine_threadsafe(
                    self.send_text_callback(text),
                    app.loop
                )
            else:
                self.logger.error("应用程序实例或事件循环不可用")
        else:
            self.logger.error("文本发送回调未设置")
    
    def toggle_auto_mode(self):
        """API方法：切换自动模式"""
        self.logger.info("API触发：切换自动聊天模式")
        if self.auto_callback:
            self.auto_callback()
        else:
            self.logger.error("自动模式回调未设置")

    def abort_current(self):
        """API方法：中断当前对话"""
        self.logger.info("API触发：中断当前对话")
        if self.abort_callback:
            self.abort_callback()
        else:
            self.logger.error("中断回调未设置")
    
    def update_status(self, status: str):
        """更新状态文本"""
        self.current_status = status
        self.logger.info(f"状态更新: {status}")
    
    def update_text(self, text: str):
        """更新TTS文本"""
        self.current_text = text
        self.logger.info(f"文本更新: {text}")
    
    def update_emotion(self, emotion_path: str):
        """更新表情"""
        # 从路径中提取表情名
        if emotion_path.endswith(".gif"):
            emotion_name = emotion_path.split("/")[-1].replace(".gif", "")
        else:
            emotion_name = emotion_path
        
        self.current_emotion = emotion_name
        self.logger.info(f"表情更新: {emotion_name}")
    
    def update_volume(self, volume):
        """更新音量"""
        self.logger.info(f"音量更新: {volume}")
    
    def start(self):
        """启动无头显示"""
        self.logger.info("无头显示模式已启动")
        # 无头模式下不需要特殊初始化
    
    def on_close(self):
        """关闭无头显示"""
        self.logger.info("无头显示模式已关闭")
        self.running = False
        
    def start_keyboard_listener(self):
        """启动键盘监听（无头模式下仅为接口实现）"""
        self.logger.debug("无头模式下不需要键盘监听")
        # 无实际操作
        
    def stop_keyboard_listener(self):
        """停止键盘监听（无头模式下仅为接口实现）"""
        self.logger.debug("无头模式下不需要停止键盘监听")
        # 无实际操作
        
    def update_button_status(self, text: str):
        """更新按钮状态（无头模式下仅为接口实现）"""
        self.logger.debug(f"按钮状态更新: {text}")
