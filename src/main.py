import subprocess
import logging
import sys

# 로깅 설정
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 실행할 스크립트 목록
scripts = [
    "src/data_merge.py",
    "src/preprocessing.py",
    "src/model_fit.py",
    "src/predict_sentiment.py"
]

def run_script(script):
    """
    주어진 Python 스크립트를 실행하는 함수

    Args:
        script (str): 실행할 스크립트 이름

    Returns:
        bool: 성공 여부 (True/False)
    """
    logging.info(f"[INFO] {script} 실행 시작...")
    print(f"[INFO] {script} 실행 중...")

    try:
        # subprocess를 이용해 외부 스크립트 실행
        result = subprocess.run([sys.executable, script], check=True, text=True, capture_output=True)

        # 실행 성공 로그 기록
        logging.info(f"[SUCCESS] {script} 실행 완료.")
        logging.info(f"[OUTPUT]\n{result.stdout}")
        print(f"[SUCCESS] {script} 실행 완료.")
        return True
    except subprocess.CalledProcessError as e:
        # 오류 발생 시 로그 기록 및 표준 에러 출력
        logging.error(f"[ERROR] {script} 실행 실패.")
        logging.error(f"[STDERR]\n{e.stderr}")
        print(f"[ERROR] {script} 실행 실패. 자세한 오류는 pipeline.log를 확인하세요.")
        return False

def main():
    """
    전체 감성 분석 파이프라인을 실행하는 메인 함수
    """
    logging.info("[INFO] 감성 분석 파이프라인 시작.")
    print("[INFO] 감성 분석 파이프라인 시작.")

    for script in scripts:
        success = run_script(script)
        if not success:
            logging.error(f"[ERROR] {script} 실행 중 오류 발생. 파이프라인을 중단합니다.")
            print(f"[ERROR] {script} 실행 중 오류 발생. 파이프라인을 중단합니다.")
            break

    logging.info("[INFO] 감성 분석 파이프라인 완료.")
    print("[INFO] 감성 분석 파이프라인 완료.")

if __name__ == "__main__":
    main()
