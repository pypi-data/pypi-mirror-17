# -*- coding: utf-8 -*-

def print_lol(the_list, indent=False, level=0):	# indent=false, level=0, ����Ʈ �ݺ� ��� �Լ� print_lol ����

	for each_item in the_list:	# each_item ���� the_list �� ����ִ� ������ŭ �ݺ�
		if isinstance(each_item, list):	# each_item �� ����Ʈ�� �´��� Ȯ�� # 
			print_lol(each_item, indent, level+1)	# indent=true ������ each_item ���� �ٽ� ����Ʈ�� �´��� �ݺ�
													# ����Ʈ ������ ��µǸ� level�� ���� 1�� ����
		else:
			if indent:
				for tab_stop in range(level):	# �ƴ϶�� level ���ڰ���ŭ tap_stop �� �ݺ��ϰ�
					print("\t", end="")	# \t�� level�� ���� ���ڸ�ŭ ���� ����Ʈ
			print(each_item) # each_item �� ����Ʈ�� �ƴϸ� �ش� ���� ����Ʈ


