from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw


def _make_image(path: Path, *, size: tuple[int, int], color: tuple[int, int, int], label: str) -> str:
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((12, 12, size[0] - 12, size[1] - 12), outline=(255, 255, 255), width=4)
    draw.text((24, size[1] // 2 - 10), label, fill=(255, 255, 255))
    image.save(path, format="JPEG", quality=90)
    return str(path)


def _make_minimal_xlsx(path: Path) -> str:
    files = {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""",
        "docProps/app.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>""",
        "docProps/core.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Generated XLSX</dc:title>
  <dc:creator>Codex</dc:creator>
</cp:coreProperties>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>""",
        "xl/styles.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border/></borders>
  <cellStyleXfs count="1"><xf/></cellStyleXfs>
  <cellXfs count="1"><xf xfId="0"/></cellXfs>
</styleSheet>""",
        "xl/worksheets/sheet1.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>Generated file</t></is></c>
      <c r="B1" t="inlineStr"><is><t>autotests</t></is></c>
    </row>
  </sheetData>
</worksheet>""",
    }
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for arcname, content in files.items():
            archive.writestr(arcname, content)
    return str(path)


def create_generated_assets(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    photos_dir = root / "photos_multi_upload"
    photos_dir.mkdir(parents=True, exist_ok=True)

    mobile_image = _make_image(
        root / "mobile_image.jpg",
        size=(1024, 768),
        color=(40, 120, 220),
        label="mobile-image",
    )
    contact_photo = _make_image(
        root / "photo.jpg",
        size=(900, 900),
        color=(80, 150, 90),
        label="contact-photo",
    )
    back_image = _make_image(
        root / "back.jpg",
        size=(1280, 720),
        color=(180, 90, 70),
        label="background",
    )
    import_xlsx = _make_minimal_xlsx(root / "import_form.xlsx")

    multi_upload_paths = []
    palette = [
        (50, 100, 180),
        (90, 150, 210),
        (120, 80, 160),
        (200, 110, 70),
        (60, 160, 120),
    ]
    for index, color in enumerate(palette, start=1):
        multi_upload_paths.append(
            _make_image(
                photos_dir / f"{index:02d}_avatar.jpg",
                size=(800, 800),
                color=color,
                label=f"avatar-{index}",
            )
        )

    return {
        "root": str(root),
        "mobile_image": mobile_image,
        "contact_photo": contact_photo,
        "back_image": back_image,
        "import_xlsx": import_xlsx,
        "photos_dir": str(photos_dir),
        "photo_paths": multi_upload_paths,
    }
