package com.Chat.Server;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import javax.swing.JTextArea;

public class ServerThread implements Runnable {
	private Socket client = null;
	private HashMap<String, ServerThread> userList = null;
	private JTextArea area = null;
	private BufferedReader receive = null;
	private BufferedReader list = null;// 获取本地用户列表
	private PrintWriter send = null;
	private boolean login = false;// 是否可以登录
	private String user;
	private String password;
	private String message = null;
	private boolean exit = false;// 接收和发送信息的关闭标识

	public ServerThread(Socket client, HashMap<String, ServerThread> userList2, JTextArea area) {
		this.client = client;
		this.userList = userList2;
		this.area = area;
	}

	public void stop() {
		try {
			this.exit = true;
			send.println("服务器已关闭\r\n");
			userList.remove(user);
			client.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void run() {
		try {
			InetAddress ip = client.getInetAddress();
			area.append(ip + " 正在连接服务端......\r\n");
			receive = new BufferedReader(new InputStreamReader(client.getInputStream()));
			send = new PrintWriter(client.getOutputStream(), true);
			logIn();// 登录

			if (login) {//登陆成功
				userList.put(user, this);
				// -------------------------- 新增：推送所有公共离线留言 --------------------------
				List<String> offlineMsgs = OfflineMessageUtil.getPublicOfflineMessages();
				if (!offlineMsgs.isEmpty()) {
					send.println("【系统提示】你有 " + offlineMsgs.size() + " 条公共离线通知：");
					for (String msg : offlineMsgs) {
						send.println(msg);
					}
					area.append(user + " 上线，推送公共离线通知 " + offlineMsgs.size() + " 条\r\n");
				}
				// ------------------------------------------------------------------------
				sendToAll("大家好！");

				final Thread re = new Thread(new Runnable() {// 实时读取消息
					public void run() {
						while (!exit) {
							try {
								message = receive.readLine();
								if (message == null) break;

								// -------------------------- 新增：判断是否发送离线留言 --------------------------
								if (message.startsWith("离线留言:")) {
									// 提取留言内容（格式：离线留言:内容）
									String content = message.substring(5).trim();
									if (!content.isEmpty()) {
										OfflineMessageUtil.savePublicOfflineMessage(user, content);
										send.println("【系统提示】公共离线留言已保存，后续上线用户会看到~");
										area.append(user + " 发布公共离线留言：" + content + "\r\n");
									} else {
										send.println("【系统提示】离线留言内容不能为空！");
									}
								} else {
									// 普通消息：群聊或私信
									if (message.startsWith("私信:")) {
										sendToP(message);
									} else {
										sendToAll(message);
									}
									area.append(user + " ：" + message + "\r\n");
								}

								if (message.equals("拜拜")) {
									userList.remove(user);
									break;
								}
							} catch (IOException e) {
								e.printStackTrace();
								break;
							}
						}
					}
				});
				re.start();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void logIn() throws IOException {
		String info = null;
		while (true) {
			File file = new File("D:\\list.txt");//与文件对照
			if (!file.exists())
				file.createNewFile();
			list = new BufferedReader(new FileReader(file));
			user = receive.readLine();
			password = receive.readLine();
			if (user == null || password == null || user.trim().isEmpty() || password.trim().isEmpty()) {
				area.append("空用户名或密码为空\r\n");
				send.println("Blank");
				continue;
			}
			while ((info = list.readLine()) != null) {
				String str[] = info.split("::");
				if (user.equals(str[0]) && password.equals(str[1]) && !checkRepetition(user)) {
					area.append(user + "::登录成功\r\n");
					login = true;
					break;
				}
			}
			if (login) {
				send.println("Success");
				return;
			} else {
				if (checkRepetition(user))
					send.println("Repetition");
				else
					send.println("Fialed");
			}
			area.append(user + "::尝试登录\r\n");
		}
	}

	public String getUser() {
		return user;
	}

	public void exit() {
		try {
			exit = true;
			userList.remove(user);
			client.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public boolean checkRepetition(String user) {
		return userList.containsKey(user);
	}

	private void send(String user, String message) {
		send.println(user + " ：" + message);
	}

	// 私信逻辑（保持原有功能）
	private void sendToP(String message) {
		String a[] = message.split(":", 3);
		if (a.length < 3) {
			send.println("【系统提示】私信格式错误，请重新发送！");
			return;
		}
		String pri[] = a[1].split("说", 1);
		if (pri.length == 0) {
			send.println("【系统提示】未指定接收方，请重新发送！");
			return;
		}
		String receiver = pri[0].trim();
		String content = a[2].trim();
		boolean isOnline = false;

		Set<String> keySet = userList.keySet();
		for (Iterator<String> it = keySet.iterator(); it.hasNext();) {
			ServerThread se = userList.get(it.next());
			if (se.user.equals(receiver)) {
				se.send.println(this.user + "私信你：" + content);
				send.println("你私信" + receiver + "说：" + content);
				isOnline = true;
				break;
			}
		}

		if (!isOnline) {
			send.println("【系统提示】对方当前不在线，私信无法发送！");
		}
	}

	// 群聊逻辑
	public void sendToAll(String message) {
		Set<String> keySet = userList.keySet();
		for (Iterator<String> it = keySet.iterator(); it.hasNext();) {
			ServerThread ser = userList.get(it.next());
			if (message.length() > 0)
				ser.send(user, message);
		}
	}
}