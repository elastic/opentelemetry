public class Hello{
  public static void main(String[] args) throws Exception {
    System.out.println("This is java app in a container");
    for(;;) {
      Thread.sleep(2000L);
      test();
    }
  }
  public static void test() {
    System.out.println("Executing test()");
  }
}
