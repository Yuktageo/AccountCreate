public class AccountMain {
    public static void main(String[] args) {
        Customer c1=new Customer("John","Doe");
        Account a1=new Account(c1,"Privileged");

        a1.setBalance(0.0);
        a1.deposit(500.0);
        Privileged p1=new Privileged(c1,"Privileged",500.0);
        p1.withdraw(1000.0);
        p1.display();
    }
}