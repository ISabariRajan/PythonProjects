
with open(filename, encoding="utf-8") as source:

    # get an iterable
    context = ET.iterparse(source, events=("start", "end"))

    # # turn it into an iterator
    # context = iter(context)

    # # get the root element
    # event, root = context.next()

    for event, elem in context:
        # do something with elem
        print(elem)
        # get rid of the elements after processing
        # root.clear()

# # etree._Element.
# with open(file=filename, mode="rb") as source:
# # etree.parse(source)
#     parser = etree.iterparse(source, tag="GTRLabData")
#     for event, element in parser:
#         gtrlab_id = element.find("GTRLab").get("id")
#         print(event, gtrlab_id)

#         element.clear()