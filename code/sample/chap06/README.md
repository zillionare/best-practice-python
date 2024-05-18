
## copilot代码自动完成功能

copilot.py对应书中第74~75页。如果你有copilot的license的话，可以把示例代码中除注释以外的代码都删除掉，看看copilot会如何生成代码。

## lint

lint.py对应书中第83页。你可以分别用以下命令进行lint，以了解pylint与pyflakes的差异：

```
pylint code/sample/chap06/lint.py
```

这将给出以下错误提示：

```
************* Module chap06.lint
code/sample/chap06/lint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
code/sample/chap06/lint.py:1:0: C0116: Missing function or method docstring (missing-function-docstring)
code/sample/chap06/lint.py:5:0: E1111: Assigning result of a function call, where the function has no return (assignment-from-no-return)
code/sample/chap06/lint.py:5:0: C0103: Constant name "value" doesn't conform to UPPER_CASE naming style (invalid-name)
```

正如书中所说，这里第4行，关于变量x与y未使用大写的警告不一定合适。

如果我们使用pyflakes来进行检查：

```
pyflakes code/sample/chap06/lint.py 
```
它将不会给出任何警告。因此，不同的工具，它们掌握的尺度是不一样的。

如果你的Python运行环境下未安装这两个工具，可以通过以下命令进行安装：

```bash
pip install pylint==3.2.0
pip install pyflakes==2.4.0
```

## typing
对应书中第86~87页。

运行命令：

```
python -m mypy mypy code/sample/chap06/typing.py 
```

你将看到以下输出(Python版本为3.11)：

```
code/sample/chap06/typing.py:5: note: Revealed type is "builtins.int"
code/sample/chap06/typing.py:7: note: Revealed type is "Any"
code/sample/chap06/typing.py:8: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
code/sample/chap06/typing.py:19: note: Revealed type is "Any"
code/sample/chap06/typing.py:19: note: 'reveal_type' always outputs 'Any' in unchecked functions
code/sample/chap06/typing.py:26: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 2 errors in 1 file (checked 1 source file)
```
