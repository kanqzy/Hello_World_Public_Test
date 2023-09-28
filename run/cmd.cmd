exit

REM src
cd /d D:\holiday\suck\Python\examples\project\JsonParse\src
python jsonParseDemo.py
python jsonOutput.py
python jsonDataVisit.py
python test.py
python jsonDataConvert.py

REM src/demo
cd /d D:\holiday\suck\Python\examples\project\JsonParse\src\demo
python treeObjToJsonStringDemo.py


REM test json data
```
                                                                // err
ABC                                                             // err
{type: "file", filepath:"D:\book\Python", value: 3}             // err
{type: "file", filepath:"D:\\book\\Python", value: 3}
{type: "file", filepath:"D:/book/Python", value: 3}
{type: 'file', filepath:'D:\book\Python', value: 3}
{"type": 'file', "filepath":'D:\book\Python', "value": 3}       // err
{"type": "file", "filepath":"D:\book\Python", "value": 3}       // err
{"type": "file", "filepath":"D:\\book\\Python", "value": 3}     // right
{"type": "file", "filepath":"D:/book/Python", "value": 3}
```

REM test\test
cd /d D:\holiday\suck\Python\examples\project\JsonParse\test\test
python test.py