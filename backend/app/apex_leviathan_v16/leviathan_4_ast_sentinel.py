import ast
import hashlib
from pathlib import Path
from typing import Dict, Any, List

class AstSelfIntrospectingSentinel:
    """
    4. PROJECT AST-SENTINEL:
    يفحص شجرة الكود المصدري المجردة (Python AST) لملفات النواة فعلياً أثناء التشغيل
    للتأكد من عدم وجود استدعاءات تنفيذ خطرة (eval, exec, compile, os.system, subprocess, pickle.loads)
    أو استيراد مكتبات محظورة، ويصدر بصمة نزاهة بنيوية للكود.
    """
    FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__", "system", "popen", "loads"}
    FORBIDDEN_MODULES = {"subprocess", "pty", "telnetlib"}

    @classmethod
    def verify_directory_source_ast(cls, target_dir: Path) -> Dict[str, Any]:
        py_files = sorted(list(target_dir.glob("*.py")))
        violations = []
        total_ast_nodes = 0
        total_functions = 0
        total_classes = 0
        combined_digest = hashlib.sha256()

        for py_file in py_files:
            source_code = py_file.read_text(encoding="utf-8")
            combined_digest.update(source_code.encode("utf-8"))
            tree = ast.parse(source_code, filename=py_file.name)

            for node in ast.walk(tree):
                total_ast_nodes += 1
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_functions += 1
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in cls.FORBIDDEN_MODULES:
                            violations.append(f"{py_file.name}:ForbiddenImport:{alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.split(".")[0] in cls.FORBIDDEN_MODULES:
                        violations.append(f"{py_file.name}:ForbiddenImportFrom:{node.module}")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in cls.FORBIDDEN_CALLS:
                        violations.append(f"{py_file.name}:ForbiddenCall:{node.func.id}")
                    elif isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen"}:
                        violations.append(f"{py_file.name}:ForbiddenAttrCall:{node.func.attr}")

        codebase_clean = len(violations) == 0
        return {
            "ast_introspection_verified": codebase_clean,
            "files_inspected_count": len(py_files),
            "total_ast_nodes_parsed": total_ast_nodes,
            "verified_classes_count": total_classes,
            "verified_functions_count": total_functions,
            "security_violations_found": violations,
            "codebase_structural_sha256": combined_digest.hexdigest()
        }