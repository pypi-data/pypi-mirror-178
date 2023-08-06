from os import PathLike
from typing import Callable, List, Union, Awaitable

import nbformat
from nbformat import NotebookNode
from nbformat.v4 import new_code_cell

from .NotebookCell import NotebookCell


class Notebook:
    """
    class for async interaction with notebooks
    """

    def __init__(self, notebook: Union[str, PathLike], ce: Callable[[NotebookCell], Awaitable], execute: bool):
        """
        :param notebook: notebook path
        :param execute: execute all cells in `__aenter__`
        :param execute: timeout per cell in seconds
        """
        self._nb: NotebookNode = nbformat.read(notebook, as_version=4)
        self._ce: Callable[[NotebookCell], Awaitable] = ce
        self._execute: bool = execute

    async def __aenter__(self) -> "Notebook":
        """
        initialize and setup kernel

        :return: self
        """
        if self._execute:
            await self.execute_cells()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        clear kernel

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        """
        pass

    async def execute_code(self, code: str) -> NotebookCell:
        """
        execute code in notebook context

        :param code: code string
        :return: cell output after execution
        """
        # create new code cell
        cell = new_code_cell(code)

        # insert into notebook
        insert_index = len(self._nb.cells)
        self._nb.cells.append(cell)

        # execute cell
        nb_cell = NotebookCell(self._nb, self._ce, insert_index)
        await nb_cell.execute()

        # parse output
        return nb_cell

    @property
    def cells(self) -> List[NotebookCell]:
        """
        get a list of all cells

        :return: list of NotebookCell
        """
        return [NotebookCell(self._nb, self._ce, i) for i in range(len(self._nb.cells))]

    def get_code_cells(self, *tag: str, from_tag: str = None, to_tag: str = None) -> List[NotebookCell]:
        """
        get code cells
          - all cells by default
          - matching at least one of the given tags if given
          - only between first occurrence of `from_tag` to first occurrence of `to_tag` if given

        :param tag: cell tags
        :param from_tag: start execution after first occurrence
        :param to_tag: stop execution after first occurrence
        :return:
        """
        result: List[NotebookCell] = []

        start_tag_found = False
        end_tag_found = False

        for cell in self.cells:
            if from_tag in cell.tags:
                start_tag_found = True
            if to_tag in cell.tags:
                end_tag_found = True

            if cell.type != 'code' or (from_tag is not None and not start_tag_found):
                continue

            if len(tag) == 0 or any([t in cell.tags for t in tag]):
                result.append(cell)

            if end_tag_found:
                break

        return result

    async def execute_cells(self, *tag: str, from_tag: str = None, to_tag: str = None) -> List[NotebookCell]:
        """
        execute code cells using `get_code_cells`

        :param tag: cell tags
        :param from_tag: start execution after first occurrence
        :param to_tag: stop execution after first occurrence
        :return:
        """
        result: List[NotebookCell] = self.get_code_cells(*tag, from_tag=from_tag, to_tag=to_tag)

        for cell in result:
            await cell.execute()

        return result
