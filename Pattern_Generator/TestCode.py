from CSVtoPD import NANDCommandLoader
import sys

if __name__ == "__main__": 
    # 커맨드라인 인자로 CSV 파일 경로 입력 받기
    if len(sys.argv) < 2:
        print("Usage: python TestCode.py <csv_path>")
        sys.exit(1)
    csv_path = sys.argv[1]
    
    # NANDCommandLoader 인스턴스 생성
    loader = NANDCommandLoader(csv_path)
    
    # CSV 파일 로드
    loader.load_csv()
    
    # 상위 5개 데이터 출력
    # loader.show_head(5)
    
    # 특정 CMD 코드로 필터링된 데이터 출력
    filtered_df = loader.filter_by_cmd("CMD_CODE")
    if filtered_df is not None:
        print(filtered_df)
    
    # 전체 DataFrame 반환
    df = loader.get_dataframe()
    print(df)