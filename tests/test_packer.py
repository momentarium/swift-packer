import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKER = REPO_ROOT / "packer.py"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_sample_project(root: Path) -> None:
    write_file(root / "AppDelegate.swift", "import UIKit\n\nfinal class AppDelegate {}\n")
    write_file(root / "Models" / "User.swift", "struct User { let id: String }\n")
    write_file(root / "Views" / "MainView.swift", "struct MainView {}\n")
    write_file(root / "Views" / "Legacy" / "LegacyView.swift", "struct LegacyView {}\n")
    write_file(root / "Mocks" / "Fake.swift", "struct Fake {}\n")
    write_file(root / "Generated" / "Thing.generated.swift", "struct GeneratedThing {}\n")
    write_file(root / "notes.txt", "not a swift file")

    write_file(root / ".git" / "config", "ignored")
    write_file(root / "Pods" / "Pod.swift", "struct Pod {}\n")
    write_file(root / ".build" / "Build.swift", "struct Build {}\n")
    write_file(root / "DerivedData" / "Derived.swift", "struct Derived {}\n")
    write_file(root / "build" / "BuildOutput.swift", "struct BuildOutput {}\n")
    write_file(root / "tests" / "Tests.swift", "struct Tests {}\n")
    write_file(root / "Fastlane" / "Fastfile", "ignored")
    write_file(root / ".xcodeproj" / "project.pbxproj", "ignored")
    write_file(root / ".xcworkspace" / "contents.xcworkspacedata", "ignored")


def run_packer(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(PACKER), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )


def test_cli_uses_current_directory_and_writes_custom_output_name(tmp_path):
    project_dir = tmp_path / "ExampleApp"
    project_dir.mkdir()
    build_sample_project(project_dir)

    result = run_packer("-o", "my_project_context.txt", cwd=project_dir)

    output_path = project_dir / "my_project_context.txt"
    assert output_path.exists()
    assert result.returncode == 0

    content = output_path.read_text(encoding="utf-8")
    assert "PROJECT STRUCTURE:" in content
    assert "Root: ExampleApp" in content
    assert "AppDelegate.swift" in content
    assert "Models/User.swift" in content
    assert "Views/MainView.swift" in content
    assert "```swift" in content
    assert "struct User { let id: String }" in content

    assert ".git" not in content
    assert "Pods/" not in content
    assert "build/" not in content
    assert "tests/" not in content
    assert "Fastlane/" not in content
    assert "notes.txt" not in content


def test_cli_accepts_project_path_and_writes_output_file_elsewhere(tmp_path):
    project_dir = tmp_path / "SampleProject"
    project_dir.mkdir()
    build_sample_project(project_dir)

    output_path = tmp_path / "bundle.txt"
    run_packer(str(project_dir), "-o", str(output_path))

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Root: SampleProject" in content
    assert "Views/MainView.swift" in content
    assert "struct MainView {}" in content


def test_custom_exclusions_support_folder_names_globs_and_relative_paths(tmp_path):
    project_dir = tmp_path / "CustomProject"
    project_dir.mkdir()
    build_sample_project(project_dir)

    run_packer(
        str(project_dir),
        "-e",
        "Mocks",
        "*.generated.swift",
        "Views/Legacy/*",
        "*Tests.swift",
    )

    output_path = project_dir / "project_bundle.txt"
    content = output_path.read_text(encoding="utf-8")

    assert "Mocks/" not in content
    assert "LegacyView.swift" not in content
    assert "Thing.generated.swift" not in content
    assert "Tests.swift" not in content
    assert "Views/MainView.swift" in content
    assert "Models/User.swift" in content


def test_default_exclusions_are_applied_to_tree_and_contents(tmp_path):
    project_dir = tmp_path / "ExcludedProject"
    project_dir.mkdir()
    build_sample_project(project_dir)

    run_packer(str(project_dir))

    output_path = project_dir / "project_bundle.txt"
    content = output_path.read_text(encoding="utf-8")

    assert "Pods/" not in content
    assert "DerivedData/" not in content
    assert ".git/" not in content
    assert "build/" not in content
    assert "tests/" not in content
    assert "Fastlane/" not in content
    assert ".xcodeproj/" not in content
    assert ".xcworkspace/" not in content

    assert "struct Pod {}" not in content
    assert "struct Derived {}" not in content
    assert "struct BuildOutput {}" not in content
    assert "struct Tests {}" not in content


def test_non_swift_text_files_can_be_excluded(tmp_path):
    project_dir = tmp_path / "ResourcesProject"
    project_dir.mkdir()

    write_file(project_dir / "StoreSync" / "Localizable.xcstrings", '"greeting" = "Hello";\n')
    write_file(project_dir / "StoreSync" / "View.swift", "struct View {}\n")

    run_packer(str(project_dir), "-e", "StoreSync/Localizable.xcstrings")

    output_path = project_dir / "project_bundle.txt"
    content = output_path.read_text(encoding="utf-8")

    assert "struct View {}" in content
    assert "greeting" not in content
    assert "Localizable.xcstrings" not in content
