# YSRes

A Parser of a certain anime game's data files (WIP)

Current target version: 3.4

## Requirements

- Python 3

- `ksdump` which is in [Kaitai Struct: visualizer](https://github.com/kaitai-io/kaitai_struct_visualizer)
```shell
gem install kaitai-struct-visualizer
```

- kaitaistruct
```shell
pip install kaitaistruct
```

## How to run

- Place binary files in `YSRes/bin` from the blks using [Studio](https://gitlab.com/RazTools/Studio)
- File structure should look like this :
```
YSRes/    (main folder)
├── bin/
│   ├── BinOutput/    (not use now, extract from 24230448.blk)
│   │   ├── ConfigAvatar_{Character}.bin
│   │   ...
│   ├── ExcelBinOutput/    (must be placed everything, extract from 25539185.blk)
│   │   ├── AvatarExcelConfigData.bin
│   │   ├── AvatarPromoteExcelConfigData.bin
│   │   ├── AvatarSkillDepotExcelConfigData.bin
│   │   ├── AvatarSkillExcelConfigData.bin
│   │   ├── AvatarTalentExcelConfigData.bin
│   │   ├── FetterInfoExcelConfigData.bin
│   │   ├── MaterialExcelConfigData.bin
│   │   └── ProudSkillExcelConfigData.bin
│   └── TextMap_{Language}/
│       ├──{anything}.bin
│       ...
├── json/    (generated files, don't remove AvatarCurveExcelConfigData.json)
├── ksy/
├── py/
├── res/    (generated files, credit to GenshinScripts)
├── character.py
├── main.py
└── README.md
```

## Future Goals

- Args support
- Tower data
- GenerateElemBall data

## Credit
- partypooper for the original [KaitaiDumper](https://github.com/partypooperarchive/KaitaiDumper)
- WeedwackerPS for the [DataParser](https://github.com/WeedwackerPS/DataParser)
- Raz for [Studio](https://gitlab.com/RazTools/Studio)
- ToaHartor for [GenshinScripts](https://github.com/ToaHartor/GenshinScripts)
