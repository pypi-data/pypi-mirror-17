# -*- coding: utf-8 -*-

def print_lol(the_list, level):	# ����Ʈ �ݺ� ��� �Լ� print_lol ����
	for each_item in the_list:	# each_item ���� the_list �� ����ִ� ������ŭ �ݺ�
		if isinstance(each_item, list):	# each_item �� ����Ʈ�� �´��� Ȯ�� # 
			print_lol(each_item, level+1)	# ������ each_item ���� �ٽ� ����Ʈ�� �´��� �ݺ�
											# ����Ʈ ������ ��µǸ� level�� ���� 1�� ����
		else:
			for tab_stop in range(level):	# �ƴ϶�� level ���ڰ���ŭ tap_stop �� �ݺ��ϰ�
				print("\t", end="")	# \t�� level�� ���� ���ڸ�ŭ ���� ����Ʈ
			print(each_item) # each_item �� ����Ʈ�� �ƴϸ� �ش� ���� ����Ʈ	