from flask import Flask, request, jsonify
import logging
import threading
from src.application import Application
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

app = Flask(__name__)

# 禁用Flask的默认日志处理器，使用我们自己的
app.logger.handlers.clear()
for handler in logging.getLogger().handlers:
    app.logger.addHandler(handler)


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取当前状态"""
    try:
        display = Application.get_instance().display
        status = {
            "status": "success",
            "device_state": str(Application.get_instance().device_state),
            "current_status": display.current_status if hasattr(display, 'current_status') else None,
            "current_text": display.current_text if hasattr(display, 'current_text') else None,
            "current_emotion": display.current_emotion if hasattr(display, 'current_emotion') else None
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/record/start', methods=['POST'])
def start_recording():
    """开始录音的API端点"""
    try:
        display = Application.get_instance().display
        if hasattr(display, 'start_recording'):
            display.start_recording()
            return jsonify({"status": "success", "message": "Recording started"})
        return jsonify({"status": "error", "message": "Not supported"}), 400
    except Exception as e:
        logger.error(f"开始录音失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/record/stop', methods=['POST'])
def stop_recording():
    """停止录音的API端点"""
    try:
        display = Application.get_instance().display
        if hasattr(display, 'stop_recording'):
            display.stop_recording()
            return jsonify({"status": "success", "message": "Recording stopped"})
        return jsonify({"status": "error", "message": "Not supported"}), 400
    except Exception as e:
        logger.error(f"停止录音失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/text', methods=['POST'])
def send_text():
    """发送文本的API端点"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "Missing text parameter"}), 400
            
        text = data.get('text', '')
        display = Application.get_instance().display
        if hasattr(display, 'send_text'):
            display.send_text(text)
            return jsonify({"status": "success", "message": "Text sent"})
        return jsonify({"status": "error", "message": "Not supported"}), 400
    except Exception as e:
        logger.error(f"发送文本失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/auto', methods=['POST'])
def toggle_auto():
    """切换自动模式的API端点"""
    try:
        display = Application.get_instance().display
        if hasattr(display, 'toggle_auto_mode'):
            display.toggle_auto_mode()
            return jsonify({"status": "success", "message": "Auto mode toggled"})
        return jsonify({"status": "error", "message": "Not supported"}), 400
    except Exception as e:
        logger.error(f"切换自动模式失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/abort', methods=['POST'])
def abort_current():
    """中断当前对话的API端点"""
    try:
        display = Application.get_instance().display
        if hasattr(display, 'abort_current'):
            display.abort_current()
            return jsonify({"status": "success", "message": "Current conversation aborted"})
        return jsonify({"status": "error", "message": "Not supported"}), 400
    except Exception as e:
        logger.error(f"中断对话失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """根路径，提供简单说明"""
    return """
    <html>
        <head><title>小智AI服务器</title></head>
        <body>
            <h1>小智AI服务器接口</h1>
            <p>可用的API端点:</p>
            <ul>
                <li>GET /api/status - 获取当前状态</li>
                <li>POST /api/record/start - 开始录音</li>
                <li>POST /api/record/stop - 停止录音</li>
                <li>POST /api/text - 发送文本（需要JSON格式：{"text": "要发送的内容"}）</li>
                <li>POST /api/auto - 切换自动模式</li>
                <li>POST /api/abort - 中断当前对话</li>
            </ul>
        </body>
    </html>
    """


def run_server(host='0.0.0.0', port=5000):
    """启动Web服务器"""
    logger.info(f"启动Web服务器在 http://{host}:{port}")
    app.run(host=host, port=port, threaded=True)
