from django.core.management.base import BaseCommand
import threading
class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
    	thread1 = Thread1();
    	thread1.start();
    	

    	thread2 = Thread2();
    	thread2.start();
    	
    	thread1.join();
    	thread2.join();



class Thread1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		for i in range(1000):
			print("Thread1 - "+str(i));
			++i;


class Thread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		for i in range(1000):
			print("Thread2 - "+str(i));
			++i;