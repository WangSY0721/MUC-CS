package com.Chat.Client;

import java.awt.*;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.JButton;
import javax.swing.JDialog;
import java.awt.event.ActionListener;
import java.net.*;
import java.io.*;
import java.awt.event.ActionEvent;
import javax.swing.JPasswordField;

public class ClientUI extends JFrame {

	private static final long serialVersionUID = -8542876911761120960L;
	private JPanel contentPane;
	private JTextField textField;
	private JPasswordField passwordField;
	private Socket client;
	private JTextField textField_1;
	private JTextField textField_2;
	private RegUI regDialog;
	private String ip = null;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ClientUI frame = new ClientUI();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public ClientUI() {
		setIconImage(
				Toolkit.getDefaultToolkit().getImage(ChatRoomUI.class.getResource("/com/Chat/Client/Chat_ico2.png")));
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setBounds(100, 100, 600, 300);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		setResizable(false);
		Font font=new Font("宋体", Font.BOLD, 20);
		setTitle("Client登录界面");
		JLabel label = new JLabel("用户名：");
		label.setFont(font);

		textField = new JTextField();
		textField.setColumns(30);

		JButton button = new JButton("登录");
		//button.setFont(font);
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {

				if (textField.getText().length() == 0 || passwordField.getPassword().length == 0) {
					Dialog errorLink = new Dialog(ClientUI.this);
					errorLink.setLayout(new FlowLayout());
					errorLink.setTitle("输入错误");
					errorLink.add(new Label("请输入用户名和密码"));
					errorLink.setBounds(600, 200, 200, 100);
					JButton liButton = new JButton("确定");
					errorLink.add(liButton);
					liButton.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							errorLink.dispose();
						}
					});
					errorLink.setVisible(true);
				} else {
					if (client != null) {
						login(textField.getText(), new String(passwordField.getPassword()));// 登录界面
					} else {
						Dialog errorLink = new Dialog(ClientUI.this);
						errorLink.setLayout(new FlowLayout());
						errorLink.setTitle("连接错误");
						errorLink.add(new Label("还没有连接服务器，请先连接！"));
						errorLink.setBounds(600, 200, 400, 100);
						JButton liButton = new JButton("确定");
						errorLink.add(liButton);
						liButton.addActionListener(new ActionListener() {
							public void actionPerformed(ActionEvent e) {
								errorLink.dispose();
							}
						});
						errorLink.setVisible(true);
					}

				}
			}

		});

		passwordField = new JPasswordField();

		JLabel label_1 = new JLabel("密码：");
		label_1.setFont(font);
		JButton button_1 = new JButton("注册");
		button_1.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent e) {
				if (client != null)
					register(client);// 注册界面
				else {
					Dialog errorLink = new Dialog(ClientUI.this);
					errorLink.setLayout(new FlowLayout());
					errorLink.setTitle("连接错误");
					errorLink.add(new Label("还没有连接服务器，请先连接！"));
					errorLink.setBounds(600, 400, 400, 100);
					JButton liButton = new JButton("确定");
					errorLink.add(liButton);
					liButton.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							errorLink.dispose();
						}
					});
					errorLink.setVisible(true);
				}

			}
		});

		textField_1 = new JTextField();
		textField_1.setText("1111");
		textField_1.setColumns(10);

		JLabel label_2 = new JLabel("端口：");
		label_2.setFont(font);
		JLabel label_3 = new JLabel("服务器：");
		label_3.setFont(font);

		textField_2 = new JTextField();
		textField_2.setText("172.27.80.1");
		textField_2.setColumns(10);

		JButton button_2 = new JButton("连接");
		button_2.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent e) {
				String ip = textField_2.getText();// 获取IP 和端口建立连接
				int port = Integer.parseInt(textField_1.getText());
				try {
					client = new Socket(ip, port);
					ClientUI.this.ip = ip;
					setTitle(getTitle() + "连接成功");
					button_2.setEnabled(false);
				} catch (UnknownHostException e1) {
					e1.printStackTrace();
				} catch (IOException e1) {
					JDialog error = new JDialog(ClientUI.this, "连接错误", true);
					error.getContentPane().add(new Label("您输入的信息有误,或服务器未开启，请重新连接"));
					error.setBounds(400, 400, 400, 200);
					error.setVisible(true);
					e1.printStackTrace();
				}
			}
		});

		GroupLayout gl_contentPane = new GroupLayout(contentPane);
		gl_contentPane.setHorizontalGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_contentPane.createSequentialGroup().addContainerGap()
						.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
								.addGroup(gl_contentPane.createSequentialGroup().addComponent(label_3)
										.addPreferredGap(ComponentPlacement.RELATED)
										.addComponent(textField_2, GroupLayout.PREFERRED_SIZE, 122,
												GroupLayout.PREFERRED_SIZE)
										.addGap(18).addComponent(label_2).addPreferredGap(ComponentPlacement.UNRELATED)
										.addComponent(textField_1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
												GroupLayout.PREFERRED_SIZE))
						.addGroup(gl_contentPane.createSequentialGroup()
								.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING).addComponent(label_1)
										.addComponent(label))
								.addPreferredGap(ComponentPlacement.RELATED)
								.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING, false)
										.addComponent(textField)
										.addComponent(passwordField, GroupLayout.DEFAULT_SIZE, 300, Short.MAX_VALUE))))
				.addGap(42).addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING).addComponent(button_1)
						.addComponent(button).addComponent(button_2)).addGap(80)));
		gl_contentPane
				.setVerticalGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
						.addGroup(gl_contentPane.createSequentialGroup().addContainerGap()
								.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE).addComponent(label_3)
										.addComponent(textField_2, GroupLayout.PREFERRED_SIZE, 22,
												GroupLayout.PREFERRED_SIZE)
						.addComponent(label_2)
						.addComponent(textField_1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
								GroupLayout.PREFERRED_SIZE).addComponent(button_2))
				.addGap(37)
				.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE).addComponent(label)
						.addComponent(button).addComponent(textField, GroupLayout.PREFERRED_SIZE,
								GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
				.addGap(19)
				.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE).addComponent(label_1)
						.addComponent(passwordField, GroupLayout.PREFERRED_SIZE, 22, GroupLayout.PREFERRED_SIZE)
						.addComponent(button_1)).addContainerGap(22, Short.MAX_VALUE)));
		contentPane.setLayout(gl_contentPane);

	}

	public void login(String name, String password) {
		try {
			PrintWriter send = new PrintWriter(client.getOutputStream(), true);
			BufferedReader receive = new BufferedReader(new InputStreamReader(client.getInputStream()));
			send.println(name);
			send.println(password);
			String info = receive.readLine();
			switch (info) {// 根据返回信息判断登录情况
			case "Success"://登录成功
				new ChatRoomUI(client, name ,ip).setVisible(true);
				dispose();
				break;
			case "Fialed":
				Dialog error = new Dialog(this, "登录错误", true);// 使用Jdialog将出现解析问题
				error.add(new Label("    帐号或密码错误，请重新登录！"));
				error.setBounds(600, 200, 290, 100);
				error.setLayout(new FlowLayout());
				JButton erButton = new JButton("确定");
				error.add(erButton);
				erButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						error.dispose();
					}
				});
				error.setVisible(true);
				break;
			case "Repetition":
				Dialog reError = new Dialog(this, "登录错误", true);
				reError.add(new Label("   您所输入的帐号已经在线，请尝试其他帐号！"));
				reError.setBounds(600, 200, 370, 100);
				reError.setLayout(new FlowLayout());
				JButton reButton = new JButton("确定");
				reError.add(reButton);
				reButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						reError.dispose();
					}
				});
				reError.setVisible(true);
				break;
			case "Blank":
				Dialog blankError = new Dialog(this, "登录错误", true);
				blankError.add(new Label("请输入用户名或密码！"));
				blankError.setBounds(600, 200, 180, 100);
				blankError.setLayout(new FlowLayout());
				JButton blButton = new JButton("确定");
				blankError.add(blButton);
				blButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						blankError.dispose();
					}
				});
				blankError.setVisible(true);
				break;
			default:
				break;
			}

		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	public void register(Socket client) {

		regDialog = new RegUI(ip);
		regDialog.setModal(true);
		regDialog.setVisible(true);
	}
}
