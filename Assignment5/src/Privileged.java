public class Privileged extends Account{



    private double overDraftLimit;

    public Privileged(Customer customer, String accountType,double overDraftLimit) {
        super(customer, accountType);
        this.overDraftLimit=overDraftLimit;
    }

    public void withdraw(double amount){
        System.out.println("Please wait while withdrawing amount "+amount);
        if (this.overDraftLimit>amount){
            this.setBalance(this.getBalance()-amount);
        }else {
            System.out.println("Amount requested is beyond limit......checking overdraft limit");
            System.out.println("TRANSACTION DENIED. Overdraft limit exceeded.");

        }
    }

    public void display(){
        System.out.println("Customer Account Name:"+customer.getFirstName()+" "+customer.getLastName());
        System.out.println("Priveleged Account Balance: -"+this.overDraftLimit);
        System.out.println("Overdraft Available Limit: "+this.overDraftLimit);

    }


}
