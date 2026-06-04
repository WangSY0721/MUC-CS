package com.Chat.Server;

import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import javax.swing.JTextArea;

public class Server extends Thread {
	private int port = 1111;
	private JTextArea area;
	private ServerSocket server;
	private boolean stop = false;
	private RegisterThread registerT;//注册线程
	private HashMap<String, ServerThread> userList = new HashMap<>();
	private ListThread listT;

	public Server(int port, JTextArea textArea) {
		this.port = port;
		this.area = textArea;
		
	}

	public void run() {
		InetAddress ip = null;
		try {
			ip = InetAddress.getLocalHost();
		} catch (UnknownHostException e1) {
			e1.printStackTrace();
		}
		try {
			server = new ServerSocket(port, 50);
			register(area);
			area.append("服务器名称：" + ip + " 端口号：" + port + "\r\n");
			area.append("服务器已经启动！\r\n");
			listT = new ListThread(userList);
			listT.start();
			int i=0;//记录线程个数
			while (!stop) {
				try {
					Socket client = server.accept();//处于阻塞状态，直接关闭将SocketServer将抛出异常
					new Thread(new ServerThread(client, userList, area), "ClientThread" + (i++)).start();
				}
				catch(Exception e)
				{
					System.out.println(e.toString());
				}
			}
		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
		}
	}

	public void register(JTextArea area) throws IOException, InterruptedException{//注册线程
		registerT=new RegisterThread(area);
		Thread.sleep(10);
		registerT.start();
	}
	
	public void exit() {//退出
		try {
			if (server != null) {
				this.stop = true;
				this.interrupt();
				registerT.interrupt();
				listT.interrupt();
				server.close();
				//server.shutdownOutput();
				Set<String> keySet = userList.keySet();
				for (Iterator<String> it = keySet.iterator(); it.hasNext();) {
					System.out.println("一次");
					userList.get(it.next()).stop();
				}
				area.append("服务器已关闭\r\n");
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
