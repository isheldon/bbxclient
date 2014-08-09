import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.print.Book;
import java.awt.print.PageFormat;
import java.awt.print.Paper;
import java.awt.print.Printable;
import java.awt.print.PrinterException;
import java.awt.print.PrinterJob;



public class PrintImg implements Printable {
   /** *//**
   * @param Graphic指明打印的图形环境
   * @param PageFormat指明打印页格式（页面大小以点为计量单位，1点为1英才的1/72，1英寸为25.4毫米。A4纸大致为595×842点）
   * @param pageIndex指明页号
   **/
   public int print(Graphics gra, PageFormat pf, int pageIndex) throws PrinterException {
       Component c = null;
      //转换成Graphics2D
      Graphics2D g2 = (Graphics2D) gra;
      //设置打印颜色为黑色
      g2.setColor(Color.black);
      //打印起点坐标
      double x = pf.getImageableX();
      double y = pf.getImageableY();
      Image src = Toolkit.getDefaultToolkit().getImage("/etc/bobox/bobox.jpg");
      g2.drawImage(src,(int)x,(int)y,c);
      return 0;
   }


  public static void main(String[] args) {
    //    通俗理解就是书、文档
    Book book = new Book();
    //    设置成竖打
    PageFormat pf = new PageFormat();
    pf.setOrientation(PageFormat.PORTRAIT);
    //    通过Paper设置页面的空白边距和可打印区域。必须与实际打印纸张大小相符。
    Paper p = new Paper();
    p.setSize(187,187);//纸张大小
    p.setImageableArea(13,30, 187,187);//A4(595 X 842)设置打印区域，其实0，0应该是72，72，因为A4纸的默认X,Y边距是72
    pf.setPaper(p);
    //    把 PageFormat 和 Printable 添加到书中，组成一个页面
    book.append(new PrintImg(), pf);
     //获取打印服务对象
     PrinterJob job = PrinterJob.getPrinterJob();
     // 设置打印类
     job.setPageable(book);

     try {
         job.print();

     } catch (PrinterException e) {
         e.printStackTrace();
     }

  }

}

