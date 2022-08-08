
import java.awt.Dialog;
import java.io.IOException;
import java.util.ArrayList;
import javax.swing.JOptionPane;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author alexl_000
 */
public class WOTD_GUI extends javax.swing.JFrame {

    /**
     * Creates new form WOTD_GUI
     */
    static DatabaseOperator database;

    public WOTD_GUI() {
        initComponents();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        AddWordsDialog = new javax.swing.JDialog();
        SubmitButton = new javax.swing.JButton();
        jScrollPane2 = new javax.swing.JScrollPane();
        WordEntryForm = new javax.swing.JTextArea();
        wordSelectionLabel = new javax.swing.JLabel();
        GoButtonCombo = new javax.swing.JButton();
        dayComboBox = new javax.swing.JComboBox();
        addWordButton = new javax.swing.JButton();
        ManualEntryField = new javax.swing.JTextField();
        GoButonField = new javax.swing.JButton();

        AddWordsDialog.setMinimumSize(new java.awt.Dimension(400, 300));

        SubmitButton.setText("Submit");
        SubmitButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SubmitButtonActionPerformed(evt);
            }
        });

        WordEntryForm.setColumns(20);
        WordEntryForm.setRows(5);
        jScrollPane2.setViewportView(WordEntryForm);

        javax.swing.GroupLayout AddWordsDialogLayout = new javax.swing.GroupLayout(AddWordsDialog.getContentPane());
        AddWordsDialog.getContentPane().setLayout(AddWordsDialogLayout);
        AddWordsDialogLayout.setHorizontalGroup(
            AddWordsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(AddWordsDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(AddWordsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(AddWordsDialogLayout.createSequentialGroup()
                        .addGap(0, 302, Short.MAX_VALUE)
                        .addComponent(SubmitButton))
                    .addComponent(jScrollPane2))
                .addContainerGap())
        );
        AddWordsDialogLayout.setVerticalGroup(
            AddWordsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(AddWordsDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 243, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(SubmitButton)
                .addContainerGap())
        );

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        wordSelectionLabel.setFont(new java.awt.Font("Tahoma", 0, 36)); // NOI18N
        wordSelectionLabel.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        wordSelectionLabel.setText("TEST");
        wordSelectionLabel.setToolTipText("");

        GoButtonCombo.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        GoButtonCombo.setText("Get Word");
        GoButtonCombo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                GoButtonComboActionPerformed(evt);
            }
        });

        dayComboBox.setFont(new java.awt.Font("Tahoma", 0, 24)); // NOI18N
        dayComboBox.setMaximumRowCount(7);
        dayComboBox.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" }));

        addWordButton.setText("Add Words");
        addWordButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addWordButtonActionPerformed(evt);
            }
        });

        GoButonField.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        GoButonField.setText("Get Word");
        GoButonField.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                GoButonFieldActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addComponent(ManualEntryField, javax.swing.GroupLayout.PREFERRED_SIZE, 134, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(wordSelectionLabel, javax.swing.GroupLayout.PREFERRED_SIZE, 578, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(152, 152, 152))
                            .addGroup(layout.createSequentialGroup()
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(GoButonField, javax.swing.GroupLayout.PREFERRED_SIZE, 103, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(addWordButton)
                        .addGap(112, 874, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(dayComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 134, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(GoButtonCombo, javax.swing.GroupLayout.PREFERRED_SIZE, 103, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(dayComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(GoButtonCombo, javax.swing.GroupLayout.DEFAULT_SIZE, 35, Short.MAX_VALUE)
                        .addGap(3, 3, 3)))
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(54, 54, 54)
                        .addComponent(wordSelectionLabel, javax.swing.GroupLayout.PREFERRED_SIZE, 320, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(11, 11, 11)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(ManualEntryField, javax.swing.GroupLayout.PREFERRED_SIZE, 36, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(GoButonField, javax.swing.GroupLayout.PREFERRED_SIZE, 39, javax.swing.GroupLayout.PREFERRED_SIZE))))
                .addGap(47, 47, 47)
                .addComponent(addWordButton)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void GoButtonComboActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_GoButtonComboActionPerformed
        String textSelection = dayComboBox.getSelectedItem().toString().toLowerCase().substring(0, 1);
        wordSelectionLabel.setText(database.SelectWord(textSelection));
    }//GEN-LAST:event_GoButtonComboActionPerformed

    private void addWordButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addWordButtonActionPerformed
        AddWordsDialog.setVisible(true);
    }//GEN-LAST:event_addWordButtonActionPerformed

    private void SubmitButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SubmitButtonActionPerformed
        String[] wordList = WordEntryForm.getText().replaceAll("[^a-zA-Z ]", "").toLowerCase().split("\\s+");
        ArrayList<String> workingList = new ArrayList<>();

        for (String x : wordList) {
            workingList.add(x);
        }
        database.AddWords(workingList);
        database.Save();
        AddWordsDialog.setVisible(false);

    }//GEN-LAST:event_SubmitButtonActionPerformed

    private void GoButonFieldActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_GoButonFieldActionPerformed
        String entryText = ManualEntryField.getText();
        wordSelectionLabel.setText(database.SelectWord(entryText));
    }//GEN-LAST:event_GoButonFieldActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) throws IOException {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(WOTD_GUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(WOTD_GUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(WOTD_GUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(WOTD_GUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        database = new DatabaseOperator("WordList.txt");

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new WOTD_GUI().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JDialog AddWordsDialog;
    public javax.swing.JButton GoButonField;
    public javax.swing.JButton GoButtonCombo;
    public javax.swing.JTextField ManualEntryField;
    public javax.swing.JButton SubmitButton;
    private javax.swing.JTextArea WordEntryForm;
    private javax.swing.JButton addWordButton;
    public javax.swing.JComboBox dayComboBox;
    private javax.swing.JScrollPane jScrollPane2;
    public javax.swing.JLabel wordSelectionLabel;
    // End of variables declaration//GEN-END:variables
}