
import csv
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps, ExifTags


# ============================================================
# CONFIGURATION
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp",
    ".bmp", ".tif", ".tiff"
}

JPEG_QUALITY = 85
WEBP_QUALITY = 80

DATETIME_ORIGINAL = 36867
DATETIME_DIGITIZED = 36868
DATETIME = 306


# ============================================================
# DATE EXTRACTION
# ============================================================

def parse_exif_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(
            str(value).strip(),
            "%Y:%m:%d %H:%M:%S"
        )
    except (ValueError, TypeError):
        return None


def get_date_taken(image_path):

    try:
        with Image.open(image_path) as img:

            exif = img.getexif()

            if not exif:
                return None, "MISSING"

            try:
                exif_ifd = exif.get_ifd(
                    ExifTags.IFD.Exif
                )
            except Exception:
                exif_ifd = {}

            date_fields = [
                (
                    exif_ifd.get(DATETIME_ORIGINAL),
                    "EXIF DateTimeOriginal"
                ),
                (
                    exif_ifd.get(DATETIME_DIGITIZED),
                    "EXIF DateTimeDigitized"
                ),
                (
                    exif.get(DATETIME),
                    "EXIF DateTime"
                ),
                (
                    exif.get(DATETIME_ORIGINAL),
                    "EXIF DateTimeOriginal"
                ),
                (
                    exif.get(DATETIME_DIGITIZED),
                    "EXIF DateTimeDigitized"
                )
            ]

            for value, source in date_fields:

                parsed = parse_exif_date(value)

                if parsed:
                    return parsed, source

    except Exception:
        pass

    return None, "MISSING"


# ============================================================
# MANUAL DATE INPUT
# ============================================================

def request_manual_date(image_path):

    print("\n" + "=" * 65)
    print("MANUAL DATE REQUIRED")
    print("=" * 65)

    print(f"Original filename: {image_path.name}")
    print("No valid capture date was found.")

    while True:

        value = input(
            "\nEnter actual date taken (DD-MM-YYYY): "
        ).strip()

        try:
            date = datetime.strptime(
                value,
                "%d-%m-%Y"
            )

            print("Date recorded successfully.")
            return date

        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY.")


# ============================================================
# IMAGE COLLECTION
# ============================================================

def collect_images(folder):

    images = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(file)

    return sorted(
        images,
        key=lambda p: p.name.lower()
    )


# ============================================================
# COLLECT ALL IMAGE DATES BEFORE PROCESSING
# ============================================================

def prepare_image_records(images):

    records = []

    print("\n" + "=" * 65)
    print("SCANNING IMAGE DATES")
    print("=" * 65)

    for index, image_path in enumerate(images, start=1):

        print(
            f"\nChecking image {index}/{len(images)}: "
            f"{image_path.name}"
        )

        capture_date, date_source = get_date_taken(
            image_path
        )

        if capture_date is None:

            capture_date = request_manual_date(
                image_path
            )

            date_source = "MANUAL"

        records.append({
            "source": image_path,
            "capture_date": capture_date,
            "date_source": date_source
        })

    return records


# ============================================================
# CHRONOLOGICAL SORTING
# ============================================================

def sort_chronologically(records):

    return sorted(
        records,
        key=lambda record: (
            record["capture_date"],
            record["source"].name.lower()
        )
    )


# ============================================================
# DISPLAY IMAGE ORDER
# ============================================================

def display_order(records):

    print("\n" + "=" * 85)
    print("PROPOSED IMAGE ORDER")
    print("=" * 85)

    print(
        f"{'No.':<6}"
        f"{'Original Filename':<38}"
        f"{'Capture Date':<22}"
        f"{'Date Source'}"
    )

    print("-" * 85)

    for index, record in enumerate(records, start=1):

        print(
            f"{index:<6}"
            f"{record['source'].name[:36]:<38}"
            f"{record['capture_date'].strftime('%d-%m-%Y %H:%M'):<22}"
            f"{record['date_source']}"
        )

    print("-" * 85)
    print(f"Total images: {len(records)}")


# ============================================================
# EDIT AN IMAGE DATE
# ============================================================

def edit_image_date(records):

    display_order(records)

    try:
        position = int(
            input("\nEnter image position to edit: ")
        )

        if not 1 <= position <= len(records):
            print("Invalid position.")
            return records

    except ValueError:
        print("Enter a valid number.")
        return records

    record = records[position - 1]

    print(f"\nSelected: {record['source'].name}")

    new_date = request_manual_date(
        record["source"]
    )

    record["capture_date"] = new_date
    record["date_source"] = "MANUAL"

    # Recalculate chronological order automatically.
    records = sort_chronologically(records)

    print("\nDate updated. Image order recalculated.")

    return records


# ============================================================
# MANUALLY MOVE AN IMAGE
# ============================================================

def move_image(records):

    display_order(records)

    try:

        current_position = int(
            input("\nImage position to move: ")
        )

        if not 1 <= current_position <= len(records):
            print("Invalid image position.")
            return records

        new_position = int(
            input("New position: ")
        )

        if not 1 <= new_position <= len(records):
            print("Invalid destination position.")
            return records

    except ValueError:
        print("Enter valid numbers.")
        return records

    image = records.pop(current_position - 1)

    records.insert(
        new_position - 1,
        image
    )

    print("\nImage moved successfully.")
    print("Manual ordering has been retained.")

    return records


# ============================================================
# REVIEW AND CONFIRM FINAL ORDER
# ============================================================

def review_final_order(records):

    records = sort_chronologically(records)

    while True:

        display_order(records)

        print("\n========== REVIEW MENU ==========")
        print("1. Change an image's date")
        print("2. Move an image to another position")
        print("3. Display the complete order")
        print("4. Confirm and start processing")
        print("5. Cancel")
        print("=================================")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":

            records = edit_image_date(records)

        elif choice == "2":

            records = move_image(records)

        elif choice == "3":

            display_order(records)

        elif choice == "4":

            print("\nFinal sequence confirmed.")
            return records, True

        elif choice == "5":

            print("\nProcessing cancelled.")
            return records, False

        else:

            print("\nInvalid option.")


# ============================================================
# ORIGINAL IMAGE
# ============================================================

def create_original(source, destination):

    shutil.copy2(source, destination)

    return destination.stat().st_size


# ============================================================
# COMPRESSED IMAGE
# ============================================================

def create_compressed(source, destination):

    original_size = source.stat().st_size

    try:

        with Image.open(source) as original:

            extension = source.suffix.lower()

            save_options = {}

            if extension in {".jpg", ".jpeg"}:

                img = original.copy()

                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")

                save_options = {
                    "format": "JPEG",
                    "quality": JPEG_QUALITY,
                    "optimize": True,
                    "progressive": True
                }

                exif = original.getexif()

                if exif:
                    save_options["exif"] = exif.tobytes()

                if original.info.get("icc_profile"):
                    save_options["icc_profile"] = (
                        original.info["icc_profile"]
                    )

            elif extension == ".png":

                img = original.copy()

                save_options = {
                    "format": "PNG",
                    "optimize": True,
                    "compress_level": 9
                }

            elif extension in {".tif", ".tiff"}:

                img = original.copy()

                save_options = {
                    "format": "TIFF",
                    "compression": "tiff_lzw"
                }

            elif extension == ".webp":

                img = original.copy()

                save_options = {
                    "format": "WEBP",
                    "quality": JPEG_QUALITY,
                    "method": 6
                }

            else:

                shutil.copy2(source, destination)

                return (
                    destination.stat().st_size,
                    "COPIED"
                )

            img.save(destination, **save_options)

        compressed_size = destination.stat().st_size

        if compressed_size >= original_size:

            destination.unlink(missing_ok=True)

            shutil.copy2(source, destination)

            return (
                destination.stat().st_size,
                "ORIGINAL_USED"
            )

        return compressed_size, "COMPRESSED"

    except Exception as error:

        destination.unlink(missing_ok=True)

        shutil.copy2(source, destination)

        return (
            destination.stat().st_size,
            f"FALLBACK_COPY: {error}"
        )


# ============================================================
# WEBP PREVIEW
# ============================================================

def create_preview(source, destination):

    with Image.open(source) as original:

        img = ImageOps.exif_transpose(original)

        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        options = {
            "format": "WEBP",
            "quality": WEBP_QUALITY,
            "method": 6
        }

        if original.info.get("icc_profile"):
            options["icc_profile"] = (
                original.info["icc_profile"]
            )

        img.save(destination, **options)

    return destination.stat().st_size


# ============================================================
# CSV REPORT
# ============================================================

def create_report(report_path, records):

    columns = [
        "Final Serial Number",
        "Original Filename",
        "Compressed Filename",
        "Capture Date",
        "Date Source",
        "Original Size (MB)",
        "Compressed Size (MB)",
        "Preview Size (MB)",
        "Compression Savings (%)",
        "Compression Status",
        "Processing Status"
    ]

    with open(
        report_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()
        writer.writerows(records)


# ============================================================
# CHECK FOR EXISTING OUTPUT FILES
# ============================================================

def check_existing_files(
    records,
    event_suffix,
    folder,
    compression_enabled
):

    original_dir = folder / "original"
    compressed_dir = folder / "compressed"
    preview_dir = folder / "preview"

    for index, record in enumerate(records, start=1):

        extension = record["source"].suffix.lower()

        name = f"{event_suffix}-{index:04d}"

        destinations = [
            original_dir / f"{name}{extension}",
            preview_dir / f"{name}.webp"
        ]

        if compression_enabled:

            destinations.append(
                compressed_dir / f"{name}{extension}"
            )

        for destination in destinations:

            if destination.exists():

                print("\nERROR: Output filename already exists.")
                print(destination)
                print(
                    "\nNo files have been processed. "
                    "Use a different event suffix or clear "
                    "the previous output files."
                )

                return False

    return True


# ============================================================
# MAIN PROCESSING
# ============================================================

def process_images(
    records,
    folder,
    event_suffix,
    compression_enabled
):

    original_dir = folder / "original"
    compressed_dir = folder / "compressed"
    preview_dir = folder / "preview"

    original_dir.mkdir(exist_ok=True)
    preview_dir.mkdir(exist_ok=True)

    if compression_enabled:
        compressed_dir.mkdir(exist_ok=True)

    report_records = []

    total_original = 0
    total_compressed = 0
    total_preview = 0

    successful = 0
    failed = 0

    print("\n" + "=" * 65)
    print("STARTING FINAL IMAGE PROCESSING")
    print("=" * 65)

    for index, record in enumerate(records, start=1):

        source = record["source"]
        extension = source.suffix.lower()

        new_name = (
            f"{event_suffix}-{index:04d}"
        )

        original_path = (
            original_dir / f"{new_name}{extension}"
        )

        compressed_path = (
            compressed_dir / f"{new_name}{extension}"
        )

        preview_path = (
            preview_dir / f"{new_name}.webp"
        )

        original_size = source.stat().st_size
        compressed_size = 0
        preview_size = 0

        compression_status = (
            "NOT_ENABLED"
            if not compression_enabled
            else "NOT_PROCESSED"
        )

        processing_status = "SUCCESS"

        print(
            f"\n[{index}/{len(records)}] "
            f"{source.name} -> {new_name}"
        )

        try:

            # Original copy
            create_original(
                source,
                original_path
            )

            # Compressed copy from untouched source
            if compression_enabled:

                compressed_size, compression_status = (
                    create_compressed(
                        source,
                        compressed_path
                    )
                )

            # Preview independently from untouched source
            preview_size = create_preview(
                source,
                preview_path
            )

            successful += 1

            print("Completed successfully.")

        except Exception as error:

            processing_status = f"FAILED: {error}"
            failed += 1

            print(f"Processing error: {error}")

        total_original += original_size
        total_compressed += compressed_size
        total_preview += preview_size

        if compression_enabled and original_size > 0:

            savings = (
                (original_size - compressed_size)
                / original_size
            ) * 100

        else:

            savings = 0

        report_records.append({

            "Final Serial Number": index,

            "Original Filename": source.name,

            "Compressed Filename": f"{new_name}{extension}",

            "Capture Date": record["capture_date"].strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            "Date Source": record["date_source"],

            "Original Size (MB)": round(
                original_size / (1024 ** 2), 3
            ),

            "Compressed Size (MB)": round(
                compressed_size / (1024 ** 2), 3
            ),

            "Preview Size (MB)": round(
                preview_size / (1024 ** 2), 3
            ),

            "Compression Savings (%)": round(
                savings, 2
            ),

            "Compression Status": compression_status,

            "Processing Status": processing_status
        })

    # CSV report
    report_path = folder / (
        f"{event_suffix}_Processing_Report.csv"
    )

    create_report(
        report_path,
        report_records
    )

    # Final summary
    print("\n" + "=" * 65)
    print("PROCESSING COMPLETED")
    print("=" * 65)

    print(f"Total images: {len(records)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    print(
        f"\nOriginal storage: "
        f"{total_original / (1024 ** 3):.3f} GB"
    )

    if compression_enabled:

        print(
            f"Compressed storage: "
            f"{total_compressed / (1024 ** 3):.3f} GB"
        )

    print(
        f"Preview storage: "
        f"{total_preview / (1024 ** 3):.3f} GB"
    )

    print("\nOutput folders:")
    print(f"Original:   {original_dir}")
    print(f"Compressed: {compressed_dir}")
    print(f"Preview:    {preview_dir}")

    print(f"\nCSV report: {report_path}")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n" + "=" * 65)
    print("CHRONOLOGICAL IMAGE ORGANIZER & CONVERTER ---- BY PADYANAVA MAITY")
    print("=" * 65)

    folder_input = input(
        "\nEnter image folder path: "
    ).strip().strip('"')

    folder = Path(folder_input)

    if not folder.is_dir():

        print("Invalid folder path.")
        return

    event_suffix = input(
        "\nEnter event suffix (e.g. DP_25): "
    ).strip()

    if not event_suffix:

        print("Event suffix cannot be empty.")
        return

    sort_choice = input(
        "\nSort images chronologically? (Y/N): "
    ).strip().lower()

    compression_choice = input(
        "Create compressed copies? (Y/N): "
    ).strip().lower()

    enable_sort = sort_choice == "y"
    enable_compression = compression_choice == "y"

    # Step 1: Collect images
    images = collect_images(folder)

    if not images:

        print("\nNo supported images found.")
        return

    print(f"\nFound {len(images)} images.")

    # Step 2: Collect dates for ALL images
    records = prepare_image_records(images)

    # Step 3: Initial chronological sorting
    if enable_sort:

        records = sort_chronologically(records)

    # Step 4: Review the complete order before processing
    records, confirmed = review_final_order(records)

    if not confirmed:
        return

    # Step 5: Check for existing output files
    if not check_existing_files(
        records,
        event_suffix,
        folder,
        enable_compression
    ):
        return

    # Step 6: Start processing only after confirmation
    process_images(
        records,
        folder,
        event_suffix,
        enable_compression
    )


if __name__ == "__main__":
    main()
