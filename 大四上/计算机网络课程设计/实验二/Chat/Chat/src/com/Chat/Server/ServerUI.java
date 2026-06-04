package com.Chat.Server;

import java.awt.EventQueue;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.border.EmptyBorder;
import javax.swing.event.CaretEvent;
import javax.swing.event.CaretListener;

public class ServerUI extends JFrame {


	private static final long serialVersionUID = -1780849261675807781L;
	private JPanel contentPane;
	private JTextField textField;
	private Server server = null;
	private JButton button_1;
	private JButton button;
	private JLabel label;
	private JScrollPane scrollPane;
	private JTextArea textArea;
	private JButton button_2;


	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ServerUI frame = new ServerUI();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}


	public ServerUI() {
		setIconImage(
				Toolkit.getDefaultToolkit().getImage(ServerUI.class.getResource("/com/Chat/Server/Chat_ico2.png")));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(260, 150, 550, 550);
		setTitle("服务器");
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(10, 10, 10, 10));
		setResizable(false);
		setContentPane(contentPane);

		label = new JLabel("  端口号：");

		textField = new JTextField();
		textField.setText("1111");
		textField.setColumns(15);
		button_1 = new JButton("关闭服务器");
		button_1.setEnabled(false);
		button = new JButton("开启服务器");

		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				startServer();
			}
		});

		button_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				stopServer();
			}
		});

		scrollPane = new JScrollPane();

		GroupLayout gl_contentPane = new GroupLayout(contentPane);
		gl_contentPane.setHorizontalGroup(gl_contentPane.createParallelGroup(Alignment.TRAILING)
				.addGroup(gl_contentPane.createSequentialGroup()
						.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
								.addGroup(gl_contentPane.createSequentialGroup().addComponent(label)
										.addPreferredGap(ComponentPlacement.RELATED)
										.addComponent(textField, GroupLayout.PREFERRED_SIZE, 200,
												GroupLayout.PREFERRED_SIZE)
										.addPreferredGap(ComponentPlacement.RELATED).addComponent(button)
										.addPreferredGap(ComponentPlacement.RELATED).addComponent(button_1))
						.addComponent(scrollPane, GroupLayout.DEFAULT_SIZE, 450, Short.MAX_VALUE)).addContainerGap()));
		gl_contentPane.setVerticalGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_contentPane.createSequentialGroup()
						.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE).addComponent(label)
								.addComponent(textField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
										GroupLayout.PREFERRED_SIZE)
								.addComponent(button).addComponent(button_1))
				.addPreferredGap(ComponentPlacement.RELATED)
				.addComponent(scrollPane, GroupLayout.DEFAULT_SIZE, 450, Short.MAX_VALUE)));

		textArea = new JTextArea();
		textArea.setLineWrap(true);
		textArea.setEditable(false);
		textArea.setCaretPosition(textArea.getText().length());
		textArea.addCaretListener(new CaretListener() {

			@Override
			public void caretUpdate(CaretEvent e) {
				//textArea.setSelectionStart(textArea.getText().length());// 设置自动换行到最后一行，有BUG
			}
		});
		scrollPane.setViewportView(textArea);// SrollPane画布会让TextArea具有滚动条效果

		contentPane.setLayout(gl_contentPane);
	}

	public void startServer() {
		if (server == null) {
			server = new Server(Integer.parseInt(textField.getText()), textArea);
			server.start();
			button.setEnabled(false);
			button_1.setEnabled(true);
		}
	}

	public void stopServer() {
		if (server != null) {
			server.exit();
			server = null;
		}
		button.setEnabled(true);
		button_1.setEnabled(false);
	}

}
