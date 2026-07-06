import io
from fastapi import FastAPI , UploadFile , HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
app = FastAPI()
@app.post("/clean")
def clean_csv(file:UploadFile):
    df= pd.read_csv(file.file)
    for col in df.columns:
            try:
                df[col] = df[col].str.strip().str.title()
            except Exception:
                pass
    cleaned_df = df.drop_duplicates()
    if len(cleaned_df) == 0:
        raise HTTPException(status_code=400 , detail="no data remaining after cleaning.")
    numeric_columns = cleaned_df.select_dtypes(include="number").columns
    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].fillna(0)
    cleaned_df = cleaned_df.fillna("N/A")
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as excel_writer:
        cleaned_df.to_excel(excel_writer, sheet_name="Cleaned Data", index=False)
    excel_buffer.seek(0)
    return StreamingResponse(excel_buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

