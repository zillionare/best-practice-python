local admonitions = {
  warning   = {pandoc.Str("警告！")},
  info        = {pandoc.Str("信息：")},
  note      = {pandoc.Str("注意！")},
  tip       = {pandoc.Str("小贴士")},
  important = {pandoc.Str("重要!")},
  caution   = {pandoc.Str("当心!")},
  cite = {pandoc.Str("引用")}
  }

function Div(el)
  local admonition_text = admonitions[el.classes[1]]
  if admonition_text then
    table.insert(el.content, 1,
        pandoc.Para{ pandoc.Strong(admonition_text) })
  end
  return el
end
