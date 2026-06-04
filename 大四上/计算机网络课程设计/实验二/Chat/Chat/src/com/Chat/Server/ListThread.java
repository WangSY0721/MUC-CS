package com.Chat.Server;

import java.io.*;
import java.net.*;
import java.util.*;

public class ListThread extends Thread {
	private HashMap<String, ServerThread> userlist;
	private ServerSocket server;
	public ListThread(HashMap<String, ServerThread> userlist) {
		
		try {
			server = new ServerSocket(34344);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.userlist = userlist;
	}
	@Override
	public void run() {
		try {
			while (true) {
				Socket client = server.accept();
				new Thread(new innerListThread(client)).start();
			}
		} catch (IOException e) {

			e.printStackTrace();
		}
	}

	private class innerListThread implements Runnable{
		private Socket client;
		private PrintWriter send;
		private StringBuilder info;
		public innerListThread(Socket client) {
			this.client=client;
		}
		
		public void run() {
			try {
				send=new PrintWriter(client.getOutputStream(),true);
				while (true) {
					try {
						Thread.sleep(1000);
						info=new StringBuilder();
						Set<String> keySet=userlist.keySet();
						Iterator<String> it=keySet.iterator();
						while (it.hasNext()) {
							info.append(it.next()+":");
						}
						send.println(info);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			} catch (IOException e) {
				
				e.printStackTrace();
			}
		}
	}

	public void exit() {
		try {
			if (server != null)
				server.close();
			server = null;
		} catch (IOException e) {

			e.printStackTrace();
		}

	}
}
