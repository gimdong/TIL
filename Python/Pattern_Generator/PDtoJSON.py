import json
import math
import pandas as pd

class NANDDataConverter:
    def __init__(self, dataframe=None):
        """
        NAND 데이터 변환기 초기화
        
        Args:
            dataframe: pandas DataFrame 객체 (선택사항)
        """
        self.df = dataframe
        self.json_data = None
        self.structured_data = None
    
    def set_dataframe(self, dataframe):
        """DataFrame 설정"""
        self.df = dataframe
    
    def remove_nan(self, d):
        """딕셔너리에서 NaN 값 제거"""
        return {k: v for k, v in d.items() if not (isinstance(v, float) and math.isnan(v))}
    
    def extract_code(self, val):
        """
        CMD(00) → 00, ADD(0A) → 0A 등에서 괄호 안 값만 추출
        괄호가 없으면 원본 반환
        """
        val = str(val)
        if '(' in val and ')' in val:
            code = val.split('(')[1].rstrip(')')
            return code.upper()
        return val.upper()
    
    def convert_row(self, row):
        """
        각 행을 구조화된 형태로 변환
        
        Args:
            row: 원본 데이터 행 (dict)
            
        Returns:
            dict: 구조화된 데이터
        """
        row = self.remove_nan(row)
        
        # CMD 값 추출 (CMD(00) → 00)
        cmd = row.get('CMD')
        cmd_val = self.extract_code(cmd) if cmd else ""
        
        # OPT_1~OPT_9, TOP_9 추출 및 변환
        opt_keys = ['OPT_1', 'OPT_2', 'OPT_3', 'OPT_4', 'OPT_5', 'OPT_6', 'OPT_7', 'OPT_8', 'TOP_9']
        opts = []
        
        for k in opt_keys:
            if k in row and row[k] is not None:
                val = str(row[k])
                if '(' in val and ')' in val:
                    type_, value = val.split('(')
                    value = value.rstrip(')')
                    # VALUE를 항상 16진수 대문자 문자열로
                    try:
                        value_hex = f"{int(value, 16):02X}"
                    except Exception:
                        value_hex = value.upper()
                    opts.append({"TYPE": type_.strip(), "VALUE": value_hex})
                else:
                    opts.append({"TYPE": val.strip(), "VALUE": ""})
        
        # 새 구조로 반환
        new_row = {
            "index": row.get("index"),
            "DESCRIPTION": row.get("DESCRIPTION"),
            "CMD": cmd_val,
            "OPT": opts
        }
        return new_row
    
    def convert_to_structured_json(self):
        """
        DataFrame을 구조화된 JSON 형태로 변환
        
        Returns:
            list: 구조화된 데이터 리스트
        """
        if self.df is None:
            raise ValueError("DataFrame이 설정되지 않았습니다. set_dataframe()을 먼저 호출하세요.")
        
        # DataFrame을 딕셔너리 리스트로 변환
        json_data = self.df.to_dict(orient='records')
        
        # 각 행을 구조화된 형태로 변환
        self.structured_data = [self.convert_row(item) for item in json_data]
        
        return self.structured_data
    
    def save_to_json(self, filepath, data=None):
        """
        JSON 파일로 저장
        
        Args:
            filepath: 저장할 파일 경로
            data: 저장할 데이터 (None이면 구조화된 데이터 사용)
        """
        if data is None:
            if self.structured_data is None:
                self.convert_to_structured_json()
            data = self.structured_data
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"[INFO] JSON 파일로 저장되었습니다: {filepath}")
    
    def convert_and_save(self, output_path):
        """
        변환 및 저장을 한 번에 수행
        
        Args:
            output_path: 출력 파일 경로
        """
        structured_data = self.convert_to_structured_json()
        self.save_to_json(output_path, structured_data)
        return structured_data

# 사용 예시:
# converter = NANDDataConverter(TestData.df)
# converter.convert_and_save('./WL_01_ver01.json')