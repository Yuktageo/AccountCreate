public class AccountMain {
    public static void main(String[] args) {

        Customer c1=new Customer();

        c1.setFirstName("John");
        c1.setLastName("Doe");

        Savings s1=new Savings(c1,"Checking");
        s1.setBalance(0.0);


        s1.deposit(1000.00);
        s1.withdraw(500.00);
        s1.display();
        System.out.println("-----------------------------------------------");
        s1.setBalance(0.0);
        s1.deposit(500.00);
        s1.withdraw(600.00);
        s1.display();
    }
}