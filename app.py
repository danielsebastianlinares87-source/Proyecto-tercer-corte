from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import os

app = Flask(__name__)

ARCHIVO = "4. ai_job_market.csv"

def cargar_df():
    if os.path.exists(ARCHIVO):
        df = pd.read_csv(ARCHIVO)
        df.columns = df.columns.str.strip()
        return df
    else:
        # estructura esperada (ajusta si tu CSV tiene columnas distintas)
        cols = ["job_id","company_name","industry","job_title","skills_required",
                "experience_level","employment_type","location","salary_range_usd",
                "posted_date","company_size","tools_preferred"]
        return pd.DataFrame(columns=cols)

def guardar_df(df):
    df.to_csv(ARCHIVO, index=False)

# RUTAS DE INTERFAZ
@app.route("/")
def index():
    df = cargar_df()
    datos = df.to_dict(orient="records")
    return render_template("index.html", datos=datos)

# CRUD (formularios HTML envían a estas rutas)
@app.route("/crear", methods=["POST"])
def crear():
    df = cargar_df()
    nuevo = {
        "job_id": request.form.get("job_id"),
        "company_name": request.form.get("company_name"),
        "industry": request.form.get("industry"),
        "job_title": request.form.get("job_title"),
        "skills_required": request.form.get("skills_required"),
        "experience_level": request.form.get("experience_level"),
        "employment_type": request.form.get("employment_type"),
        "location": request.form.get("location"),
        "salary_range_usd": request.form.get("salary_range_usd"),
        "posted_date": request.form.get("posted_date"),
        "company_size": request.form.get("company_size"),
        "tools_preferred": request.form.get("tools_preferred")
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    guardar_df(df)
    return redirect("/")

@app.route("/editar", methods=["POST"])
def editar():
    df = cargar_df()
    try:
        job_id = request.form.get("job_id")
        columna = request.form.get("columna")
        nuevo_valor = request.form.get("nuevo_valor")
        if columna in df.columns:
            mask = df["job_id"].astype(str) == str(job_id)
            df.loc[mask, columna] = nuevo_valor
            guardar_df(df)
    except Exception:
        pass
    return redirect("/")

@app.route("/eliminar", methods=["POST"])
def eliminar():
    df = cargar_df()
    try:
        job_id = request.form.get("job_id")
        df = df[df["job_id"].astype(str) != str(job_id)]
        guardar_df(df)
    except Exception:
        pass
    return redirect("/")

# API: lista de ofertas (JSON)
@app.route("/api/ofertas", methods=["GET"])
def api_ofertas():
    df = cargar_df()
    return jsonify(df.to_dict(orient="records"))

# -----------------------------
# API de análisis (1-17)
# Cada endpoint devuelve JSON con la información necesaria
# para que el frontend construya tablas o gráficas.
# -----------------------------

def parse_salary_range(s):
    # devuelve (min, max) o (None,None)
    try:
        s = str(s)
        parts = [p.strip() for p in s.split("-") if p.strip() != ""]
        if len(parts) == 2:
            return float(parts[0]), float(parts[1])
        if len(parts) == 1:
            v = float(parts[0])
            return v, v
    except Exception:
        pass
    return None, None

@app.route("/api/analyze/<int:opt>", methods=["GET"])
def api_analyze(opt):
    df = cargar_df()

    # asegurar columnas y tipos sin romper si faltan
    def safe_col(col):
        return col in df.columns

    # 1 Cantidad total de ofertas
    if opt == 1:
        return jsonify({"total": int(len(df))})

    # 2 Industria con mayor numero de empresas activas
    if opt == 2 and safe_col("industry"):
        vc = df["industry"].dropna().astype(str).value_counts()
        top = vc.idxmax() if not vc.empty else None
        return jsonify({"industry_top": top, "counts": vc.to_dict()})

    # 3 Numero de ofertas por industria
    if opt == 3 and safe_col("industry"):
        vc = df["industry"].dropna().astype(str).value_counts()
        return jsonify({"by_industry": vc.to_dict()})

    # 4 Numero de ofertas por nivel de experiencia
    if opt == 4 and safe_col("experience_level"):
        vc = df["experience_level"].dropna().astype(str).value_counts()
        return jsonify({"by_experience": vc.to_dict()})

    # 5 Numero de ofertas por tipo de contrato
    if opt == 5 and safe_col("employment_type"):
        vc = df["employment_type"].dropna().astype(str).value_counts()
        return jsonify({"by_contract": vc.to_dict()})

    # 6 Promedio del rango salarial
    if opt == 6 and safe_col("salary_range_usd"):
        salarios = []
        for s in df["salary_range_usd"].fillna(""):
            mn, mx = parse_salary_range(s)
            if mn is not None and mx is not None:
                salarios.append((mn + mx) / 2.0)
        promedio = sum(salarios)/len(salarios) if salarios else None
        return jsonify({"promedio": promedio, "samples_count": len(salarios)})

    # 7 Top 5 cargos mas comunes
    if opt == 7 and safe_col("job_title"):
        vc = df["job_title"].dropna().astype(str).value_counts().head(5)
        return jsonify({"top5_titles": vc.to_dict()})

    # 8 Top 5 empresas con mas ofertas
    if opt == 8 and safe_col("company_name"):
        vc = df["company_name"].dropna().astype(str).value_counts().head(5)
        return jsonify({"top5_companies": vc.to_dict()})

    # 9 Ofertas con salario maximo y minimo
    if opt == 9 and safe_col("salary_range_usd"):
        mins = []
        maxs = []
        for idx, s in df["salary_range_usd"].fillna("").items():
            mn, mx = parse_salary_range(s)
            mins.append((idx, mn))
            maxs.append((idx, mx))
        # filtrar None
        maxs_valid = [(i, v) for i, v in maxs if v is not None]
        mins_valid = [(i, v) for i, v in mins if v is not None]
        if not maxs_valid or not mins_valid:
            return jsonify({"max": None, "min": None})
        max_idx, max_val = max(maxs_valid, key=lambda x: x[1])
        min_idx, min_val = min(mins_valid, key=lambda x: x[1])
        row_max = df.loc[max_idx].to_dict()
        row_min = df.loc[min_idx].to_dict()
        return jsonify({"max": {"value": max_val, "row": row_max}, "min": {"value": min_val, "row": row_min}})

    # 10 Cantidad de ofertas que requieren habilidades específicas (query param ?skill=python)
    if opt == 10 and safe_col("skills_required"):
        skill = request.args.get("skill", "").strip().lower()
        if not skill:
            return jsonify({"error": "provide skill param, e.g. ?skill=python"}), 400
        count = int(df["skills_required"].dropna().astype(str).apply(lambda s: skill in s.lower()).sum())
        return jsonify({"skill": skill, "count": count})

    # 11 Cantidad de ofertas por ciudad
    if opt == 11 and safe_col("location"):
        ciudades = df["location"].fillna("").astype(str).apply(lambda x: x.split(",")[0].strip() if x else "Sin especificar").value_counts()
        return jsonify({"by_city": ciudades.to_dict()})

    # 12 Numero de habilidades mas demandadas (top N)
    if opt == 12 and safe_col("skills_required"):
        topn = int(request.args.get("topn", 10))
        listas = df["skills_required"].dropna().astype(str).apply(lambda s: [h.strip().lower() for h in s.split(",") if h.strip() != ""])
        if listas.empty:
            return jsonify({"top": {}})
        todas = []
        for lst in listas:
            todas.extend(lst)
        series = pd.Series(todas).value_counts().head(topn)
        return jsonify({"top_skills": series.to_dict()})

    # 13 Cantidad de ofertas segun tamaño de empresa
    if opt == 13 and safe_col("company_size"):
        vc = df["company_size"].dropna().astype(str).value_counts()
        return jsonify({"by_company_size": vc.to_dict()})

    # 14 Salario promedio estimado por nivel de experiencia
    if opt == 14 and safe_col("salary_range_usd") and safe_col("experience_level"):
        df_copy = df.copy()
        df_copy["sal_prom"] = df_copy["salary_range_usd"].fillna("").apply(lambda s: (lambda mn,mx: (mn+mx)/2 if mn is not None and mx is not None else None)(*parse_salary_range(s)))
        res = df_copy.dropna(subset=["sal_prom"]).groupby("experience_level")["sal_prom"].mean()
        return jsonify({"avg_salary_by_experience": res.to_dict()})

    # 15 Cantidad de ofertas publicadas por año
    if opt == 15 and safe_col("posted_date"):
        try:
            anos = pd.to_datetime(df["posted_date"], errors="coerce").dt.year
            vc = anos.value_counts().sort_index()
            return jsonify({"by_year": vc.to_dict()})
        except Exception:
            return jsonify({"error": "posted_date parsing failed"}), 500

    # 16 Analisis de habilidades laborales (global)
    if opt == 16 and safe_col("skills_required"):
        skill = request.args.get("skill", "").strip().lower()
        listas = df["skills_required"].dropna().astype(str).apply(lambda s: [h.strip().lower() for h in s.split(",") if h.strip() != ""])
        todas = []
        for lst in listas:
            todas.extend(lst)
        series = pd.Series(todas).value_counts()
        mean = series.mean() if not series.empty else 0
        if skill:
            freq = int(series.get(skill, 0))
            # classification
            if series.empty:
                level = "no_data"
            elif freq > mean * 1.5:
                level = "alta"
            elif freq < mean * 0.5:
                level = "baja"
            else:
                level = "media"
            return jsonify({"skill": skill, "freq": freq, "level": level, "top": series.head(20).to_dict()})
        else:
            return jsonify({"top_skills": series.head(50).to_dict()})

    # 17 Analisis de habilidades por ubicacion (requires skill & location query params)
    if opt == 17 and safe_col("skills_required") and safe_col("location"):
        skill = request.args.get("skill", "").strip().lower()
        location = request.args.get("location", "").strip().lower()
        if not skill or not location:
            return jsonify({"error": "provide skill and location params, e.g. ?skill=python&location=bogota"}), 400
        df_loc = df[df["location"].fillna("").astype(str).str.lower().str.contains(location)]
        listas = df_loc["skills_required"].dropna().astype(str).apply(lambda s: [h.strip().lower() for h in s.split(",") if h.strip() != ""])
        todas = []
        for lst in listas:
            todas.extend(lst)
        series = pd.Series(todas).value_counts()
        freq = int(series.get(skill, 0))
        return jsonify({"skill": skill, "location": location, "freq_in_location": freq, "top_in_location": series.head(20).to_dict()})

    return jsonify({"error": "option not implemented or missing required columns"}), 400


if __name__ == "__main__":
    app.run(debug=True)
