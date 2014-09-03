import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import javax.imageio.ImageIO;
import javax.imageio.ImageReadParam;
import javax.imageio.ImageReader;
import javax.print.DocFlavor;
import javax.print.DocPrintJob;
import javax.print.PrintService;
import javax.print.PrintServiceLookup;
import javax.print.SimpleDoc;
import javax.print.attribute.HashDocAttributeSet;
import javax.print.attribute.HashPrintRequestAttributeSet;
import javax.print.attribute.standard.MediaPrintableArea;
import javax.print.attribute.standard.MediaSizeName;
import javax.print.attribute.standard.PrintQuality;
import javax.print.attribute.standard.PrinterIsAcceptingJobs;

public class GenerateImage {
	/*
	 * 以下单位是mm（定位打印纸位置）
	 */
	private static final int LENGTH = 66;
	
	private static final int HIGH = 91;
	
	private static final int X = 4;
	
	private static final int Y = 8;
	
	/*
	 * 以下单位是像素（定位剪接图片位置）
	 */
	private int cutX;
	
	private int cutY;
	
	private int cutLength;
	
	private int height;
	
	private int blank;
	
	/*
	 * 打印的文字
	 */
	private WordPrinted wordPrinted;
	
	/*
	 * 打印的图片
	 */
	private BufferedImage bufferedImage;
	
	/*
	 * 下部图片的背景颜色
	 */
	private Color bgColor = Color.WHITE;
	
	/*
	 * 新图片位置
	 */
	public static String imagePath = "/tmp/999.";
	
	/*
	 * 图片格式的枚举
	 */
	public enum ImageFormatter {
		JPEG, PNG
	}

	public void setBgColor(Color bgColor) {
		this.bgColor = bgColor;
	}

	/*
	 * 下面两个是构造器
	 */
	public GenerateImage() {
	}
	
	public GenerateImage(int cutX, int cutY,int cutLength, WordPrinted wordPrinted, BufferedImage bufferedImage) {
		this.cutX = cutX;
		this.cutY = cutY;
		this.cutLength = cutLength;
		this.height = (int) (cutLength / 3.3);
		this.blank = height / 4;
		this.wordPrinted = wordPrinted;
		this.bufferedImage = bufferedImage;
		
		if(wordPrinted != null && bufferedImage != null) {
			wordPrinted.setFont(new Font(wordPrinted.getFontName(), wordPrinted.getFontStyle(), (int) ((cutLength - height) / wordPrinted.getWordNumPerLine() * WordPrinted.PER)));
		}
		if(wordPrinted != null && bufferedImage == null) {
			wordPrinted.setFont(new Font(wordPrinted.getFontName(), wordPrinted.getFontStyle(), (int) (cutLength / wordPrinted.getWordNumPerLine() * WordPrinted.PER)));
		}
	}

	
	/**
	 * 将图片进行剪接处理
	 */
	public String genPic(FileInputStream fis, String filename, boolean forPrint) throws Exception {
		int wth = 720;
		int hgt = 950;
		int margin = 40;
		if (forPrint) {
			wth = 1904;
			hgt = 2694;
			margin = 0;
		}

		// 剪切后的图片
		BufferedImage biu = cutPic(fis, "jpg");
		// 新图片
		BufferedImage bin = new BufferedImage(wth, hgt, BufferedImage.TYPE_INT_RGB);
		
		Graphics2D g2d = (Graphics2D) bin.getGraphics();
		g2d.setPaint (new Color (255, 255, 255));
		g2d.fillRect (0, 0, wth, hgt);
		// 将剪切后的图片画入上部
		g2d.drawImage(biu, margin, margin, null);
		/*
		 * 画入空白
		 */
		g2d.setBackground(Color.WHITE);
		g2d.clearRect(0, cutLength, cutLength + margin, blank);
		/*
		 * 画入下部图片的背景
		 */
		g2d.setBackground(bgColor);
		g2d.clearRect(0, cutLength + blank, cutLength, height);
		
		/*
		 * 根据传入的参数决定文字和图片的打印
		 */
		if(wordPrinted != null && bufferedImage != null) {
			g2d.drawImage(createPic(), margin, cutLength + blank, null);
			// 在文字和图片都有的情况下，将图片缩放在右侧
			BufferedImage bil = changePicPx(bufferedImage, height, height);
			g2d.drawImage(bil, cutLength - height, cutLength + blank, null);
		} else if(wordPrinted != null && bufferedImage == null) {
			g2d.drawImage(createPic(), margin, cutLength + blank, null);
		} else if(wordPrinted == null && bufferedImage != null) {
			// 将图片缩放为合适尺寸
			BufferedImage bil = changePicPx(bufferedImage, cutLength, height);
			g2d.drawImage(bil, margin, cutLength + blank, null);
		}

		// 输出的新图片文件位置
		String path = "/tmp/" + filename;
		FileOutputStream fos = new FileOutputStream(path);
		ImageIO.write(bin, "jpg", fos);
		fis.close();
		fos.close();
		return path;
	} 
	
	/**
	 * 裁剪图片
	 */
	private BufferedImage cutPic(FileInputStream fis, String formatter) throws Exception {
		ImageReader ir = ImageIO.getImageReadersByFormatName(formatter).next();
		ir.setInput(ImageIO.createImageInputStream(fis), true);
		ImageReadParam irp = ir.getDefaultReadParam();
		// 设置裁剪的区域
		Rectangle rt = new Rectangle(cutX, cutY, cutLength, cutLength);
		irp.setSourceRegion(rt);
		return ir.read(0, irp);
	}
	
	/**
	 * 很据文字创建图片
	 */
	private BufferedImage createPic() {
		BufferedImage bid = new BufferedImage(cutLength, height, BufferedImage.TYPE_INT_RGB);
		Graphics2D g2d = (Graphics2D) bid.getGraphics();
		/*
		 * 图片的背景
		 */
		g2d.setBackground(bgColor);
		g2d.clearRect(0, 0, cutLength, height);
		
		g2d.setPaint(wordPrinted.getFontColor());
		g2d.setFont(wordPrinted.getFont());
		int fontPx = (int) (wordPrinted.getFont().getSize() / WordPrinted.PER);
		/*
		 * 如果文字超出限制将换行
		 */
		if(getWordLength(wordPrinted.getWord()) > wordPrinted.getWordNumPerLine()) {
			// 第一行文字
			String wordF = subStr(wordPrinted.getWord(), 0, wordPrinted.getWordNumPerLine());
			// 第二行文字
			String wordS = wordPrinted.getWord().substring(wordF.length());
			// 由于只保留两行的文字，第二行超出的部分将被剪掉
			if(getWordLength(wordS) > wordPrinted.getWordNumPerLine()) {
				wordS = subStr(wordS, 0, wordPrinted.getWordNumPerLine());
			}
			g2d.drawString(wordF, 0, fontPx * 4 / 3);
			g2d.drawString(wordS, 0, fontPx * 8 / 3);
		} else {
			g2d.drawString(wordPrinted.getWord(), 0, fontPx * 4 / 3);
		}
		
		return bid;
	}
	
	/**
	 * 缩放图片
	 */
	private BufferedImage changePicPx(BufferedImage bufferedImage, int w, int h) {
		BufferedImage bi = new BufferedImage(w, h, BufferedImage.TYPE_INT_BGR);
		bi.createGraphics().drawImage(bufferedImage, 0, 0, w, h, null);;
		
		return bi;
	}
	
	private int getWordLength(String s) {
		int length = 0;
		for(int i = 0; i < s.length(); i ++) {
			if((int)s.charAt(i) < 128) {
				length += 1;
			} else {
				length += 3;
			}
		}
		return length / 3;
	}
	
	private String subStr(String s, int begin, int end) {
		int length = 0;
		for(int i = begin; i < s.length(); i ++) {
			if(length >= (end - begin) * 3) {
				return  s.substring(begin, i);
			}
			if((int)s.charAt(i) < 128) {
				length += 1;
			} else {
				length += 3;
			}
		}
		
		return s;
		
	}
	
	public static void main(String[] args) { //arg0: image path, arg1: words, arg2: adimg
		try {
			int cutLength = 640;
			int cutX = 0;
			int cutY = 0;

			WordPrinted pw = new WordPrinted();
			pw.setFontColor(Color.BLACK);
			pw.setWord(args[1]);

			BufferedImage adimg = null;
			if (args.length > 2) {
				adimg = ImageIO.read(new FileInputStream(args[2]));
			}
			
			// PrintImage pi = new PrintImage(cutX, cutY, cutLength, pw, null);
			// pi.setBgColor(new Color(153, 102, 102));
			// int result = pi.print(new FileInputStream(args[0]), ImageFormatter.JPEG);

			GenerateImage gi = new GenerateImage(cutX, cutY, cutLength, pw, adimg);
			gi.setBgColor(Color.WHITE);
			// generate image for printing
			gi.genPic(new FileInputStream(args[0]), "999.jpg", true);
			// generate image for display
			gi.genPic(new FileInputStream(args[0]), "lomoprinting.jpg", false);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
