# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        
        # strip all whitespace from the strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip() 

        # Category and product_type ----> lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
            
        # availability string
        availability_string = adapter.get('availability')
        split_string = availability_string.split('(') 
        if len(split_string) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        return item
