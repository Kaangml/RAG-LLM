import pandas as pd
from typing import List, Dict, Optional

class CSVReader:
    @staticmethod
    def extract_rows_from_csv(csv_path: str, columns_to_combine: Optional[List[str]] = None, separator: str = " | ") -> List[str]:
        """
        CSV dosyasından satırları okur ve her satırı tek bir belge olarak döndürür.
        
        Args:
            csv_path: CSV dosyasının yolu
            columns_to_combine: Birleştirilecek sütun isimleri. None ise tüm sütunlar birleştirilir.
            separator: Sütunlar arasında kullanılacak ayırıcı
            
        Returns:
            Her satırın tek bir string olarak temsil edildiği liste
        """
        try:
            # CSV dosyasını oku
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            # Boş satırları temizle
            df = df.dropna(how='all')
            
            documents = []
            
            # Eğer belirli sütunlar belirtilmişse sadece onları kullan
            if columns_to_combine:
                # Belirtilen sütunların varlığını kontrol et
                missing_cols = [col for col in columns_to_combine if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Şu sütunlar CSV'de bulunamadı: {missing_cols}")
                df_to_use = df[columns_to_combine]
            else:
                df_to_use = df
            
            # Her satırı tek bir belge olarak işle
            for idx, row in df_to_use.iterrows():
                # NaN değerleri boş string yap
                row = row.fillna('')
                
                # Sütun adı ve değerlerini birleştir
                row_parts = []
                for col_name, value in row.items():
                    if value and str(value).strip():  # Boş değerleri atla
                        row_parts.append(f"{col_name}: {value}")
                
                # Satırı birleştir
                if row_parts:  # Eğer satırda veri varsa
                    document = separator.join(row_parts)
                    documents.append(document)
            
            return documents
            
        except Exception as e:
            raise Exception(f"CSV okuma hatası: {str(e)}")
    
    @staticmethod
    def get_csv_columns(csv_path: str) -> List[str]:
        """
        CSV dosyasındaki sütun isimlerini döndürür.
        
        Args:
            csv_path: CSV dosyasının yolu
            
        Returns:
            Sütun isimleri listesi
        """
        try:
            df = pd.read_csv(csv_path, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            raise Exception(f"CSV sütunları okunamadı: {str(e)}")
    
    @staticmethod
    def preview_csv(csv_path: str, n_rows: int = 5) -> pd.DataFrame:
        """
        CSV dosyasının ilk n satırını gösterir.
        
        Args:
            csv_path: CSV dosyasının yolu
            n_rows: Gösterilecek satır sayısı
            
        Returns:
            DataFrame
        """
        try:
            df = pd.read_csv(csv_path, nrows=n_rows)
            return df
        except Exception as e:
            raise Exception(f"CSV önizleme hatası: {str(e)}")
