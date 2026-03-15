"""양도소득세 자동계산 프로그램 진입점

실행 방법:
  cd C:\\Users\\서초로\\CPA
  python -m yangdose.main
"""
import sys
import os
import logging
from datetime import datetime

# 패키지 경로 설정 (직접 실행 시)
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # 폴더명이 'yangdose'가 아닌 경우에도 yangdose 패키지로 인식되도록 등록
    folder_name = os.path.basename(current_dir)
    if folder_name != 'yangdose':
        import types
        yangdose_pkg = types.ModuleType('yangdose')
        yangdose_pkg.__path__ = [current_dir]
        yangdose_pkg.__file__ = os.path.join(current_dir, '__init__.py')
        sys.modules['yangdose'] = yangdose_pkg

# PyQt5 플러그인 경로 설정 (Qt platform plugin 오류 해결)
try:
    import PyQt5
    pyqt5_path = os.path.dirname(PyQt5.__file__)
    qt5_plugins_path = os.path.join(pyqt5_path, 'Qt5', 'plugins')
    qt5_bin_path = os.path.join(pyqt5_path, 'Qt5', 'bin')

    # QT_PLUGIN_PATH 환경 변수 설정
    os.environ['QT_PLUGIN_PATH'] = qt5_plugins_path

    # PATH에 Qt5 bin 디렉토리 추가
    if qt5_bin_path not in os.environ['PATH']:
        os.environ['PATH'] = qt5_bin_path + os.pathsep + os.environ['PATH']
    print(f"[SETUP] Qt 플러그인 경로: {qt5_plugins_path}")
except Exception as e:
    print(f"[WARNING] Qt 경로 설정 실패: {e}")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from yangdose.gui.main_window import MainWindow


def setup_debug_logging():
    """디버그 로깅 설정"""
    log_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "yangdose_logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"yangdose_debug_{datetime.now():%Y%m%d_%H%M%S}.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"{'='*80}")
    logger.info(f"양도소득세 자동계산 프로그램 시작")
    logger.info(f"로그 파일: {log_file}")
    logger.info(f"{'='*80}")

    print(f"\n{'='*80}")
    print(f"디버그 로깅 활성화됨")
    print(f"로그 파일: {log_file}")
    print(f"{'='*80}\n")

    return log_file


def main():
    # 디버그 로깅 설정
    log_file = setup_debug_logging()

    # 고DPI 지원
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
