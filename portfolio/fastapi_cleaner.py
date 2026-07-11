import io
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd

app = FastAPI()

@app.post("/clean")
def clean_csv(file: UploadFile):

    # ── Read uploaded CSV ────────────────────────────────────────
    df = pd.read_csv(file.file)

    # ── Clean text columns ───────────────────────────────────────
    for col in df.columns:
        try:
            df[col] = df[col].str.strip().str.title()
        except Exception:
            pass

    # ── Remove duplicates ────────────────────────────────────────
    cleaned_df = df.drop_duplicates()

    # ── Guard against empty result ───────────────────────────────
    if len(cleaned_df) == 0:
        raise HTTPException(status_code=400, detail="no data remaining after cleaning.")

    # ── Fill empty cells ─────────────────────────────────────────
    numeric_columns = cleaned_df.select_dtypes(include="number").columns
    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].fillna(0)
    cleaned_df = cleaned_df.fillna("N/A")

    # ── Write cleaned data to Excel in memory ────────────────────
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as excel_writer:
        cleaned_df.to_excel(excel_writer, sheet_name="Cleaned Data", index=False)

    # ── Return the file ──────────────────────────────────────────
    excel_buffer.seek(0)
    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
