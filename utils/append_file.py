import aiofiles


from typing import NoReturn


async def append_file(file_path: str, file_content: str) -> NoReturn:
    async with aiofiles.open(file=file_path,
                             mode='a',
                             encoding='utf-8') as file:
        await file.write(file_content)
