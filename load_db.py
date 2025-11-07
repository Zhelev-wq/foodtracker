import time
import sys
import uuid
from typing import List, Optional
import gc
import polars as pl
from sqlalchemy.dialects.postgresql import insert

from app.validators.food import Food as FoodValidator
from app.db.database import Session, engine
from app.db.tables import Food, Vitamins, Minerals, Fats


# =============================================================================
# CONFIGURATION
# =============================================================================
COMMIT_BATCH_SIZE = 1000
POLARS_BATCH_SIZE = 100_000

OFF_TO_ORM_MAPPING = {
    "product_name": "name",
    "carbohydrates_100g": "carbs",
    "proteins_100g": "protein",
    "fat_100g": "fat",
    "energy-kcal_100g": "kcal",
    "alcohol_100g": "alcohol",
    "caffeine_100g": "caffeine",
    "code": "barcode",
    "vitamin-a_100g": "vit_a",
    "vitamin-b1_100g": "vit_b1",
    "vitamin-b2_100g": "vit_b2",
    "vitamin-pp_100g": "vit_b3",
    "pantothenic-acid_100g": "pantothenic_acid",
    "vitamin-b6_100g": "vit_b6",
    "biotin_100g": "biotin",
    "vitamin-b9_100g": "vit_b9",
    "vitamin-b12_100g": "vit_b12",
    "vitamin-c_100g": "vit_c",
    "vitamin-d_100g": "vit_d",
    "vitamin-e_100g": "vit_e",
    "vitamin-k_100g": "vit_k",
    "calcium_100g": "calcium",
    "magnesium_100g": "magnesium",
    "phosphorus_100g": "phosphorus",
    "sodium_100g": "sodium",
    "iron_100g": "iron",
    "zinc_100g": "zinc",
    "copper_100g": "copper",
    "manganese_100g": "manganese",
    "molybdenum_100g": "molybdenum",
    "selenium_100g": "selenium",
    "iodine_100g": "iodine",
    "fluoride_100g": "fluoride",
    "chromium_100g": "chromium",
    "potassium_100g": "potassium",
    "taurine_100g": "taurine",
    "saturated-fat_100g": "saturated_fat",
    "monounsaturated-fat_100g": "monounstaurated_fat",
    "polyunsaturated-fat_100g": "polyunsaturated_fat",
    "omega-3-fat_100g": "omega_3_fat",
    "omega-6-fat_100g": "omega_6_fat",
    "omega-9-fat_100g": "omega_9_fat",
    "trans-fat_100g": "trans_fat",
}

SCHEMA_OVERRIDES = {
    'energy-kcal_100g': pl.Float64,
    'carbohydrates_100g': pl.Float64,
    'proteins_100g': pl.Float64,
    'fat_100g': pl.Float64,
    'alcohol_100g': pl.Float64,
    'code': pl.Utf8,
}


# =============================================================================
# DATABASE
# =============================================================================
def has_data(d: dict | None) -> bool:
    return d is not None and any(v is not None for v in d.values())


def commit_batch(food_items: List[FoodValidator]) -> int:
    if not food_items:
        return 0

    food_records = []
    vitamins_records = []
    minerals_records = []
    fats_records = []

    for item in food_items:
        data = item.model_dump()
        food_id = uuid.uuid4()

        food_records.append({
            'id': food_id,
            'name': data['name'],
            'carbs': data['carbs'],
            'protein': data['protein'],
            'fat': data['fat'],
            'kcal': data['kcal'],
            'alcohol': data.get('alcohol'),
            'caffeine': data.get('caffeine'),
            'barcode': data['barcode'],
        })

        if has_data(data.get('vitamins')):
            vitamins_records.append({'id': food_id, **data['vitamins']})
        if has_data(data.get('minerals')):
            minerals_records.append({'id': food_id, **data['minerals']})
        if has_data(data.get('fats')):
            fats_records.append({'id': food_id, **data['fats']})

    with Session() as session:
        session.execute(insert(Food), food_records)
        if vitamins_records:
            session.execute(insert(Vitamins), vitamins_records)
        if minerals_records:
            session.execute(insert(Minerals), minerals_records)
        if fats_records:
            session.execute(insert(Fats), fats_records)
        session.commit()

    return len(food_records)

# =============================================================================
# DATA PROCESSING
# =============================================================================
def transform_chunk(chunk: pl.DataFrame) -> pl.DataFrame:
    """Filter, rename, and structure a chunk."""
    
    filtered = chunk.filter(
        pl.col("product_name").is_not_null() &
        pl.col("carbohydrates_100g").is_not_null() &
        pl.col("proteins_100g").is_not_null() &
        pl.col("fat_100g").is_not_null() &
        pl.col("energy-kcal_100g").is_not_null() &
        (pl.col("carbohydrates_100g") >= 0) &
        (pl.col("proteins_100g") >= 0) &
        (pl.col("fat_100g") >= 0) &
        (pl.col("energy-kcal_100g") >= 0) &
        (pl.col("energy-kcal_100g") <= 900) &  # Max is pure fat at 900 kcal/100g
        ((pl.col("carbohydrates_100g") + pl.col("proteins_100g") + pl.col("fat_100g")) <= 100.0)
    )
    
    renamed = filtered.rename(OFF_TO_ORM_MAPPING)

    return renamed.select([
        pl.col("name"),
        pl.col("carbs"),
        pl.col("protein"),
        pl.col("fat"),
        pl.col("kcal").cast(pl.Float64),
        pl.col("alcohol").cast(pl.Float64),
        pl.col("caffeine").cast(pl.Float64),
        pl.col("barcode").cast(pl.String),
        pl.struct([
            "vit_a", "vit_b1", "vit_b2", "vit_b3", "pantothenic_acid",
            "vit_b6", "biotin", "vit_b9", "vit_b12", "vit_c", "vit_d", "vit_e", "vit_k"
        ]).alias("vitamins"),
        pl.struct([
            "calcium", "magnesium", "phosphorus", "sodium", "iron", "zinc",
            "copper", "manganese", "molybdenum", "selenium", "iodine",
            "fluoride", "chromium", "potassium", "taurine"
        ]).alias("minerals"),
        pl.struct([
            "saturated_fat", "monounstaurated_fat", "polyunsaturated_fat",
            "omega_3_fat", "omega_6_fat", "omega_9_fat", "trans_fat"
        ]).alias("fats"),
    ])


# =============================================================================
# MAIN
# =============================================================================
def main(file_path: str):
    reader = pl.read_csv_batched(
        source=file_path,
        separator="\t",
        batch_size=POLARS_BATCH_SIZE,
        schema_overrides=SCHEMA_OVERRIDES,
        quote_char=None,
        columns=list(OFF_TO_ORM_MAPPING.keys()),
    )

    total_committed = 0
    batch_buffer = []
    start_time = time.time()

    print(f"Importing {file_path}")

    while True:
        batches = reader.next_batches(1)
        if not batches:
            break

        chunk = transform_chunk(batches[0])
        records = chunk.to_dicts()
        
        del chunk  # Free immediately
        del batches

        for record in records:
            try:
                batch_buffer.append(FoodValidator(**record))
            except Exception:
                continue

            if len(batch_buffer) >= COMMIT_BATCH_SIZE:
                total_committed += commit_batch(batch_buffer)
                batch_buffer.clear()

        del records
        gc.collect()  # Force cleanup after each polars batch

        if total_committed % 10000 == 0:
            print(f"Committed {total_committed:,}")

    if batch_buffer:
        total_committed += commit_batch(batch_buffer)

    print(f"✓ Done: {total_committed:,} records in {time.time() - start_time:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])