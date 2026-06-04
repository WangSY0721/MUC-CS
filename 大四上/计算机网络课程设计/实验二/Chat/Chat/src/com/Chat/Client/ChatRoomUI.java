package com.Chat.Client;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;;

import javax.swing.DefaultListModel;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.border.EmptyBorder;

public class ChatRoomUI extends JFrame {

	private static final long serialVersionUID = -607104815605494438L;
	private JPanel contentPane;
	private ClientThread client;
	private JTextArea textArea_1;
	private JTextArea textArea;
	private DefaultListModel<String> model;
	private JList<String> jList;
	private Socket listSocket;
	private String ip;
	private JLabel onlineNum;
	private String user;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ChatRoomUI frame = new ChatRoomUI();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public ChatRoomUI(Socket client, String name, String ip) {
		this();
		this.user = name;
		setTitle(user + " 的聊天室");
		this.client = new ClientThread(client, textArea, this);
		this.client.start();// 开启线程
		this.ip = ip;
		try {
			this.listSocket = new Socket(ip, 34344);// 在线用户列表线程
		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public ChatRoomUI() {
		setIconImage(
				Toolkit.getDefaultToolkit().getImage(ChatRoomUI.class.getResource("/com/Chat/Client/Chat_ico2.png")));
		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		setBounds(100, 100, 1200, 900);
		setResizable(false);
		Font font1 = new Font("宋体", Font.BOLD, 15);
		Font font2 = new Font("宋体", Font.BOLD, 20);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(20, 20, 20, 20));
		setContentPane(contentPane);

		JScrollPane scrollPane = new JScrollPane();
		JScrollPane scrollPane_1 = new JScrollPane();
		JButton button = new JButton("发送");
		button.setFont(font1);
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				sendMessage();
			}
		});

		JButton button_1 = new JButton("离开");
		button_1.setFont(font1);
		button_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (client != null) {
					client.Exit();
					System.exit(0);
				}
			}
		});

		JScrollPane scrollPane_2 = new JScrollPane();

		JLabel label = new JLabel("在线人数");
		Font font = new Font("宋体", Font.BOLD, 20);
		label.setFont(font);

		onlineNum = new JLabel("0");
		onlineNum.setFont(font);

		JButton btnNewButton = new JButton("帮助");
		btnNewButton.setFont(font1);
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JDialog help = new JDialog(ChatRoomUI.this, "帮助", true);
				help.setLayout(new FlowLayout());
				JLabel helpContent3 = new JLabel("双击列表中的姓名，可单独发送私信。");
				JLabel helpContent4 = new JLabel("输入格式「离线留言:内容」，可发布公共离线通知。");
				JLabel helpContent6 = new JLabel("Ctrl+Enter快捷键可以快速发送信息。");
				help.setBounds(200, 200, 350, 200);
				help.setResizable(false);
				help.add(helpContent3);
				help.add(helpContent4);
				help.add(helpContent6);
				help.setVisible(true);
			}
		});

		// 布局设置
		GroupLayout gl_contentPane = new GroupLayout(contentPane);
		gl_contentPane.setHorizontalGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_contentPane.createSequentialGroup()
						.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING, false)
								.addComponent(scrollPane, 0, 0, Short.MAX_VALUE)
								.addGroup(gl_contentPane.createSequentialGroup().addGap(2).addComponent(scrollPane_1,
										GroupLayout.PREFERRED_SIZE, 900, GroupLayout.PREFERRED_SIZE)))
						.addGap(6)
						.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
								.addComponent(scrollPane_2, GroupLayout.DEFAULT_SIZE, 400, Short.MAX_VALUE)
								.addGroup(gl_contentPane.createSequentialGroup()
										.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
												.addComponent(label, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE,
														Short.MAX_VALUE)
												.addComponent(btnNewButton))
										.addPreferredGap(ComponentPlacement.RELATED)
										.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING).addComponent(onlineNum)))
								.addComponent(button_1, GroupLayout.DEFAULT_SIZE, 300, Short.MAX_VALUE)
								.addComponent(button, GroupLayout.DEFAULT_SIZE, 300, Short.MAX_VALUE)).addContainerGap()));
		gl_contentPane.setVerticalGroup(gl_contentPane.createParallelGroup(Alignment.LEADING).addGroup(gl_contentPane
				.createSequentialGroup()
				.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
						.addComponent(scrollPane, GroupLayout.PREFERRED_SIZE, 650, GroupLayout.PREFERRED_SIZE)
						.addGroup(gl_contentPane.createSequentialGroup()
								.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
										.addGroup(gl_contentPane.createSequentialGroup().addGap(33)
												.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE)
														.addComponent(label).addComponent(onlineNum))
												.addGap(13))
										.addGroup(gl_contentPane.createSequentialGroup()
												.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE)
														.addComponent(btnNewButton))
												.addGap(38)))
								.addPreferredGap(ComponentPlacement.UNRELATED).addComponent(scrollPane_2,
										GroupLayout.PREFERRED_SIZE, 580, GroupLayout.PREFERRED_SIZE)))
				.addPreferredGap(ComponentPlacement.RELATED)
				.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING, false)
						.addComponent(scrollPane_1, GroupLayout.PREFERRED_SIZE, 150, GroupLayout.PREFERRED_SIZE)
						.addGroup(Alignment.TRAILING, gl_contentPane.createSequentialGroup()
								.addComponent(button, GroupLayout.PREFERRED_SIZE, 43, GroupLayout.PREFERRED_SIZE)
								.addPreferredGap(ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
								.addComponent(button_1, GroupLayout.PREFERRED_SIZE, 43, GroupLayout.PREFERRED_SIZE)))
				.addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));

		// 关闭窗口事件
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				if (client != null) {
					client.Exit();
					dispose();
				}
			}
		});

		// 消息输入框
		textArea_1 = new JTextArea();
		textArea_1.setFont(font2);
		textArea_1.setLineWrap(true);
		textArea_1.addKeyListener(new KeyAdapter() {
			public void keyPressed(KeyEvent e) {
				if (e.isControlDown() && (e.getKeyCode() == KeyEvent.VK_ENTER)) {
					sendMessage();
				}
			}
		});
		scrollPane_1.setViewportView(textArea_1);

		// 消息显示区
		textArea = new JTextArea();
		textArea.setFont(font2);
		textArea.setLineWrap(true);
		textArea.setEditable(false);
		scrollPane.setViewportView(textArea);

		// 在线用户列表
		model = new DefaultListModel<>();
		jList = new JList<>(model);
		scrollPane_2.setViewportView(jList);
		jList.setFont(font2);
		jList.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				if (e.getClickCount() == 2) {
					int index = jList.locationToIndex(e.getPoint());
					String obj = model.getElementAt(index);
					if (!obj.equals(user)) {
						textArea_1.append("私信:" + obj + "说:");
						textArea_1.setCaretPosition(textArea_1.getText().length());
					}
				}
			}
		});

		contentPane.setLayout(gl_contentPane);
		new Thread(new innerRoomThread()).start();
	}

	// 发送消息封装
	private void sendMessage() {
		String message = textArea_1.getText().trim();
		if (!message.isEmpty()) {
			client.send(message);
			textArea_1.setText("");
			textArea.setCaretPosition(textArea.getText().length());
		}
	}

	// 在线列表刷新线程
	private class innerRoomThread implements Runnable {
		private BufferedReader receive;

		public void run() {
			try {
				Thread.sleep(100);
				System.out.println(listSocket.getInetAddress() + "正在获取在线列表......");
				receive = new BufferedReader(new InputStreamReader(listSocket.getInputStream()));
				String info = null;
				String list[] = null;
				while ((info = receive.readLine()) != null) {
					list = info.split(":");
					model.clear();
					for (String name : list) {
						if (!name.trim().isEmpty()) {
							model.add(model.size(), name);
						}
					}
					jList.setModel(model);
					onlineNum.setText(list.length + "");
				}
			} catch (IOException | InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}