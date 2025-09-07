import pandas as pd



class NANDCommandLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
        # 너비 제한 해제
        pd.set_option('display.width', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)

    def load_csv(self):
        """CSV 파일을 DataFrame으로 로드합니다."""
        self.df = pd.read_csv(self.csv_path)
        self.df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)  # 빈 문자열을 NA로 대체
        print(f"[INFO] CSV 파일이 성공적으로 로드되었습니다: {self.csv_path}")

    def show_head(self, n=5):
        """상위 n개의 데이터를 출력합니다."""
        if self.df is not None:
            print(self.df.head(n))
        else:
            print("[WARN] DataFrame이 로드되지 않았습니다.")

    def filter_by_cmd(self, cmd_code: str):
        """CMD 열을 기준으로 필터링된 DataFrame을 반환합니다."""
        if self.df is not None:
            return self.df[self.df['CMD'] == cmd_code]
        else:
            print("[ERROR] DataFrame이 로드되지 않았습니다.")
            return None

    def get_dataframe(self):
        """전체 DataFrame을 반환합니다."""
        return self.df