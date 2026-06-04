package com.Chat.Server;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

import javax.swing.JTextArea;
//注册线程
public class RegisterThread extends Thread {
	private ServerSocket register;
	private JTextArea area;

	public RegisterThread() {
		try {
			this.register = new ServerSocket(34343);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public RegisterThread(JTextArea area) {
		this();
		this.area = area;
	}

	@Override
	public void run() {
		while (true) {
			try {
				Socket reC = register.accept();
				area.append(reC.getInetAddress().toString());
				area.append(reC.getLocalAddress() + "正在注册\r\n");
				new Thread(new Reg(reC)).start();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	private class Reg implements Runnable {
		private Socket reC;
		private BufferedReader receive;
		private BufferedReader list;
		private PrintWriter send;
		private boolean exist = false;
		private PrintWriter writerList;

		public Reg(Socket reC) {
			this.reC = reC;
		}

		@Override
		public void run() {
			try {
				receive = new BufferedReader(new InputStreamReader(reC.getInputStream()));
				send = new PrintWriter(reC.getOutputStream(), true);
				area.append("正在读取用户列表......\r\n");
				File file = new File("D:\\list.txt");
				if (!file.exists())
					file.createNewFile();
				area.append("读取到用户列表\r\n");
				while (true) {
					synchronized (file) {// 锁住注册文件
						list = new BufferedReader(new FileReader(file));
						area.append("正在获取注册信息......");

						String name = receive.readLine();
						String password = receive.readLine();
						String info = null;
						while ((info = list.readLine()) != null) {// 与list.txt中的信息对比
							String str[] = info.split("::");
							if (str[0].equals(name)) {
								send.println("Exist");
								exist = true;
								area.append(name + "用户已经存在!\r\n");
								break;
							}
						}
						area.append(name + "::" + password + "\r\n");
						if (!exist) {
							area.append("正在写入数据.....\r\n");
							writerList = new PrintWriter(new FileOutputStream("D:\\list.txt", true), true);
							writerList.println(name + "::" + password);
							send.println("RegisterSuccess");
							area.append("写入完成\r\n");
						}

					}
				}
			} catch (IOException e) {
				e.printStackTrace();
			}

		}
	}
}
