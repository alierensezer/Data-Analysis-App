from cx_Freeze import setup, Executable

setup(
    name="EndKal Veri Analizi Uygulaması",
    version="1.0",
    description="Veri analizi uygulaması",
    executables=[Executable("veri.py", base="Win32GUI")]
)
