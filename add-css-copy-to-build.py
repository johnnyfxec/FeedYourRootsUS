import os

build_py_path = os.path.join('build', 'build.py')
with open(build_py_path, encoding='utf-8') as f:
    content = f.read()

old_main_start = '''def main():
    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source directory not found: {SRC_DIR}")
        print("Create src/about.html, src/privacy.html, src/terms.html, src/refunds.html")
        return
    built = 0'''

new_main_start = '''def copy_shared_css():
    src_css = os.path.join(BUILD_DIR, "shared.css")
    dst_css = os.path.join(OUT_DIR, "shared.css")
    if not os.path.exists(src_css):
        print(f"WARN: {src_css} not found, skipping copy")
        return
    with open(src_css, encoding="utf-8") as f:
        css_content = f.read()
    with open(dst_css, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"OK   copied shared.css -> repo root ({len(css_content)} bytes)")


def main():
    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source directory not found: {SRC_DIR}")
        print("Create src/about.html, src/privacy.html, src/terms.html, src/refunds.html")
        return
    copy_shared_css()
    built = 0'''

assert old_main_start in content, "Pattern not found — aborting"
content = content.replace(old_main_start, new_main_start)

with open(build_py_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK — build.py now auto-copies shared.css to repo root on every run")
