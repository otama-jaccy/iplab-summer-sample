from stores.ImageStore import ImageStore

s = ImageStore.get_instance()
value = s.get_value()
print(value)
value.append(1)
print(s.get_value())
print(value)

#ImageStore()