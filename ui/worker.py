from pathlib import Path
from typing import List, Tuple, Optional

from PySide6.QtCore import QThread, Signal

from ui.constants import PIL_FORMAT_MAP


class ConversionWorker(QThread):
    file_started = Signal(int)                  # row index
    file_done    = Signal(int, bool, str)        # index, success, out_path_or_err
    all_done     = Signal(int, int)              # converted_count, failed_count

    def __init__(
        self,
        tasks: List[Tuple[int, str]],   # [(row_index, input_path), ...]
        output_ext: str,
        output_folder: Optional[str],   # None → same folder as each input
        quality: int,
    ):
        super().__init__()
        self.tasks         = tasks
        self.output_ext    = output_ext
        self.output_folder = output_folder
        self.quality       = quality
        self._abort        = False

    def abort(self):
        self._abort = True

    def run(self):
        from convert import convert_image

        pil_fmt    = PIL_FORMAT_MAP.get(self.output_ext, self.output_ext.upper())
        converted  = 0
        failed     = 0

        for idx, in_path in self.tasks:
            if self._abort:
                break

            self.file_started.emit(idx)

            try:
                stem      = Path(in_path).stem
                out_dir   = self.output_folder or str(Path(in_path).parent)
                out_name  = f"{stem}.{self.output_ext}"
                out_path  = str(Path(out_dir) / out_name)

                # Avoid overwriting the source file
                if Path(out_path).resolve() == Path(in_path).resolve():
                    out_name = f"{stem}_converted.{self.output_ext}"
                    out_path = str(Path(out_dir) / out_name)

                ok = convert_image(in_path, out_path, pil_fmt)
                if ok:
                    converted += 1
                    self.file_done.emit(idx, True, out_path)
                else:
                    failed += 1
                    self.file_done.emit(idx, False, "Conversion failed")
            except Exception as exc:
                failed += 1
                self.file_done.emit(idx, False, str(exc))

        self.all_done.emit(converted, failed)
