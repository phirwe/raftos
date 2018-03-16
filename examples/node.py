import argparse
import asyncio
from datetime import datetime
import random

import raftos


class FTStack():
    
    async def sCreate(self, label):
        stack_id = random.randint(1, 10000)
        self.data_list = raftos.ReplicatedList(name='data_list')
        self.label_dict = raftos.ReplicatedDict(name='label_dict')
        return stack_id

    async def sId(self, label):
        return await self.label_dict[label]

    async def sPush(self, stack_id, item):
        data_map = {
            int(stack_id) : int(item)
        }
            
        await self.data_list.append(data_map)

    async def sPop(self, stack_id):
        length = await self.data_list.length()
        for i in range(length-1, -1, -1):
            dict_item = await self.data_list[i]
            
            if int(stack_id) in dict_item.keys():
                item = dict_item[int(stack_id)]
                await self.data_list.delete(dict_item)
                return item
            elif str(stack_id) in dict_item.keys():
                item = dict_item[str(stack_id)]
                await self.data_list.delete(dict_item)
                return int(item)

    async def sTop(self, stack_id):
        length = await self.data_list.length()
        
        for i in range(length-1, -1, -1):
            
            dict_item = await self.data_list[i]
            print (dict_item)
            if str(stack_id) in dict_item.keys():
                return dict_item[str(stack_id)]
            elif int(stack_id) in dict_item.keys():
                return dict_item[int(stack_id)]


    async def sSize(self, stack_id):
        length = 0
        total_length = await self.data_list.length()
        for i in range(total_length-1, -1, -1):
            dict_item = await self.data_list[i]
            
            if int(stack_id) in dict_item.keys():
                length += 1
            elif str(stack_id) in dict_item.keys():
                length += 1
        
        return length

    async def print_stack(self, stack_id):
        length = await self.data_list.length()
        
        for i in range(length):
            dict_item = await self.data_list[i]
            
            if int(stack_id) in dict_item.keys():
                print (dict_item[int(stack_id)], end=' ')
            elif str(stack_id) in dict_item.keys():
                print (dict_item[str(stack_id)], end=' ')




#data_dict = dict()
#label_dict = dict()
#stack_id = ""
#label = 0
#data_list = []
ftstack = FTStack()
async def run(node_id):
    
    labels = [1, 2]
    stack = []

    label = random.randint(1, 1000)
    stack_id = await ftstack.sCreate(labels[0])
#    print (stack_id)
    if stack_id != "":
        await raftos.wait_until_leader(node_id)
        await ftstack.label_dict.update({labels[0] : stack_id})
        stack.append(stack_id)
        print ("Stack ID:", stack_id)

        i = 0
        while i != 5:
            print (await ftstack.sId(labels[0]))

            item = random.randint(1, 1000000)

            print ("LENGTH BEFORE PUSH:", await ftstack.sSize(stack_id))

            print ("PUSH:", item)

            await ftstack.sPush(stack_id, item)

            item = await ftstack.sTop(stack_id)

            print ("TOP:", item)

            length = await ftstack.sSize(stack_id)

            if length % 3 == 0:
                print ("LENGTH AFTER PUSH / BEFORE POP:", await ftstack.sSize(stack_id))

                item = await ftstack.sPop(stack_id)

                print ("POP", item)

                print ("LENGTH AFTER POP:", await ftstack.sSize(stack_id))

            await ftstack.print_stack(stack_id)
            print ()
            await asyncio.sleep(2)
            i += 1
    i = 0
    stack_id = await ftstack.sCreate(labels[1])
    #    print (stack_id)
    if stack_id != "":
        await raftos.wait_until_leader(node_id)
        await ftstack.label_dict.update({labels[1] : stack_id})
        stack.append(stack_id)
        print ("Stack ID:", stack_id)
        i = 0
        while i != 4:
            print (await ftstack.sId(labels[1]))
            
            item = random.randint(1, 1000000)
            
            print ("LENGTH BEFORE PUSH:", await ftstack.sSize(stack_id))
            
            print ("PUSH:", item)
            
            await ftstack.sPush(stack_id, item)
            
            item = await ftstack.sTop(stack_id)
            
            print ("TOP:", item)
            
            length = await ftstack.sSize(stack_id)
            
            if length % 3 == 0:
                print ("LENGTH AFTER PUSH / BEFORE POP:", await ftstack.sSize(stack_id))
                
                item = await ftstack.sPop(stack_id)
                
                print ("POP", item)
                
                print ("LENGTH AFTER POP:", await ftstack.sSize(stack_id))
            
            await ftstack.print_stack(stack_id)
            print ()
            await asyncio.sleep(2)
            i += 1
    while i <= 10:
        print ("Printing stacks: ", stack, "\n\n")
        await ftstack.print_stack(stack[0])
        print ()
        await ftstack.print_stack(stack[1])
        print ()
        i += 10
        await asyncio.sleep(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--node')
    parser.add_argument('--cluster')
    args = parser.parse_args()

    cluster = ['127.0.0.1:{}'.format(port) for port in args.cluster.split()]
    node = '127.0.0.1:{}'.format(args.node)

    raftos.configure({
        'log_path': './',
        'serializer': raftos.serializers.JSONSerializer
    })

    loop = asyncio.get_event_loop()
    loop.create_task(raftos.register(node, cluster=cluster))
    loop.run_until_complete(run(node))
